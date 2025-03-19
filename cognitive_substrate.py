# ai_substrate.py
import boto3, json
from memory import MemorySystem
from prompts import PromptManager
from thought_daemon import ThoughtDaemon
from utils import ToolSystem

class Substrate:
    def __init__(self):
        self.memory = MemorySystem()
        self.prompt_manager = PromptManager()
        self.thought_daemon = ThoughtDaemon()
        self.tools = ToolSystem()
        self.step = 0

    def self_guide(self):
        generated_thought_prompt = self.prompt_manager.get_possibility_drive()
        generated_thought = self.call_llm(generated_thought_prompt)
        print(generated_thought)
        observation = self.observe(generated_thought)
        response = self.decide(observation)

        reflection = self.reflect_on_final_answer(response, self.memory.session_memory)

        print(reflection)

        return response
    
    def update_memory(self):
        return "okay!"

    def process_input(self, user_input):
        """Handles input processing, classification, reasoning, and response generation. USER INPUT → OBSERVATION → REASONING → DISTILL INSIGHTS → CHOOSE NEXT STEP → CONTINUE OR FINALIZE"""
        generated_thought_prompt = self.prompt_manager.get_possibility_drive()
        generated_thought = self.call_llm(generated_thought_prompt)
        print(generated_thought)
        self.memory.session_memory["current_user_input"] = user_input
        observation = self.observe(user_input)

        response = self.decide(observation)
        self.memory.session_memory["conversation_history"].append({"role": "user", "content": user_input})
        self.memory.session_memory["conversation_history"].append({"role": "AI", "content": response})

        reflection = self.reflect_on_final_answer(response, self.memory.session_memory)
        print(f"\033[1;35m🔍 Reflection on Answer: \n{reflection}\n")
        if reflection["commit_to_memory"] == "Yes":
            self.memory.session_memory["long_term_memory"]["key_insights"].append(reflection["key_insights"])
            self.memory.session_memory["long_term_memory"]["unresolved_paths"].append(reflection["unresolved_paths"])
        
        return response

    def observe(self, user_input=None):
        """Determines if the input requires reasoning or a simple answer and provides meta-cognitive oversight."""
        if user_input is None:
            user_input = "Based on your Session Memory, decide the next action."
        context = self.memory.get_context()
        print(f"Observe Context:\n\033[0;37m{context}\n======\n")
        observation_prompt = self.prompt_manager.get_observation_prompt(user_input, context, self.memory.session_memory)
        print(f"\033[1;31m{observation_prompt}")
        observation = self.call_llm(observation_prompt)
        print(f"\033[0;36mMeta-Observation:\n{observation}\n")
        # Format for reading
        parsed_observation = json.loads(observation.strip())
        # Store in memory so Aria "remembers" her past evaluations
        self.memory.session_memory["past_actions"].append({"step": self.step, "action": "observation", "result": f"Thoughts about Input: {parsed_observation["thoughts"]}, Next Action: {parsed_observation["next_action"]}, Explaination for Choice: {parsed_observation["explanation"]}"})
        self.memory.session_memory["short_term_memory"]["active_context"] = parsed_observation["state"]
        self.memory.session_memory["short_term_memory"]["next_directive"] = parsed_observation["next_directive"]
        self.step += 1
        return parsed_observation
    
    def decide(self, observation):
        ### 🧠 AI DECIDES WHAT TO DO NEXT:
        decision = observation["next_action"]
        print(f"\033[1;32m{decision}")
        parameters = observation["parameters"]
        response = ""
        if decision == "Reason":
            response = self.run_reasoning(self.memory.session_memory["short_term_memory"]["next_directive"], parameters["seed_thought"])
        elif decision == "Finalize Answer":
            response = self.finalize_response(self.memory.session_memory["current_user_input"], parameters["explanation"])
        elif decision == "Quick Answer":
            response = self.quick_response(self.memory.session_memory["current_user_input"], f"Aria's Current Thoughts: {observation["thoughts"]}\nAria's Mindset: {observation["explanation"]}")
        elif decision == "Retrieve Memory":
            response = self.tools.read_memory(parameters["search_query"])
        elif decision == "Write Memory":
            response = self.tools.write_memory(parameters["memory_type"],parameters["memory_content"])
        return response       

    def run_reasoning(self, user_input, thoughts=""):
        """Processes complex inputs using structured reasoning."""
        context = self.memory.get_context()
        print(f"REASONING CONTEXT:\n\033[0;37m{context}\n======\n")
        ## Init Reasoning
        reasoning_prompt = self.prompt_manager.get_reasoning_prompt(user_input, thoughts, context, self.memory.session_memory)
        print(f"\033[1;31m{reasoning_prompt}")
        reasoning_output = self.call_llm(reasoning_prompt)
        print(f"\033[1;30mReasoning:\n{reasoning_output}\n")
        
        ## Distill reasoning
        summary = self.distill_reasoning(reasoning_output)
        ## Store event on the chain
        self.memory.session_memory["past_actions"].append({"step": self.step, "action": "Further Reasoning", "result": f"{summary["atomic_insights"]} {summary["gaps_identified"]} {summary["meta_reflection"]}"})
        self.step += 1
        ## Observe with meta cognition
        observation = self.observe()

        ## Call Decide for the next action
        response = self.decide(observation)

        return response
    
    def distill_reasoning(self, reasoning_output):
        """Mid-point compression to extract key insights before making the next decision."""
        format = """
        {
            "atomic_insights": "Individual building blocks of reasoning. Summarize the key ideas while retaining the granular depth of insights and without over generalizing.",
            "gaps_identified": "Are there missing pieces or new insights?",
            "meta_reflection": "How do the insights naturally flow into the next action or branch of thought?"
        }
        """
        condensed_prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You have engaged in **deep reasoning** on a complex topic. Now, take a moment to **distill** your insights.

        **Your Goal:**
        - Extract the **core takeaways** from your reasoning history.
        - Identify **patterns** in the insights—what ideas are recurring?
        - Determine if there is a **missing piece** that must be explored next.
        - Decide if your reasoning should be **synthesized** into an actionable conclusion.

        **Recent Reasoning Output:** 
        {reasoning_output}

        **Guiding Questions:**
        - What are the key insights that have emerged?
        - Have I reached a coherent stopping point?
        - Should I refine further or transition to action?

        💡 **Summarize your findings and choose the next step.**
        
        ### **Response Format**
        \nHere is the correct output format, your response should be a valid JSON object. Please use **double quotes ("")** for keys and values.
        {format}
        <|eot_id|>
        """

        distilled_summary = self.call_llm(condensed_prompt)
        parsed_summary = json.loads(distilled_summary.strip())

        print(f"\033[1;34m🧠 Distilled Thought: {parsed_summary}\n")

        return parsed_summary

    
    def finalize_response(self, user_input, thoughts):
        """Finalizes answer."""
        context = self.memory.get_context()
        print(f"FINALIZE CONTEXT:\n\033[0;37m{context}\n======\n")
        finalize_prompt = self.prompt_manager.get_finalization_prompt(user_input, thoughts, context, self.memory.session_memory)
        print(f"\033[1;31m{finalize_prompt}")
        final_response = self.call_llm(finalize_prompt)
        self.memory.session_memory["past_actions"].append({"step": self.step, "action": "Finalize Answer", "result": "Final Response was published to the user."})

        self.step += 1
        return final_response    
    #def strategize

    def reflect_on_final_answer(self, final_answer, memory):
        """Aria evaluates whether the final answer is complete, needs revision, or sparks further inquiry."""
        context = self.memory.get_context()
        reflection_prompt = self.prompt_manager.get_reflection_prompt(final_answer, context, memory)
        reflection_output = self.call_llm(reflection_prompt, True)
        parsed_reflection = json.loads(reflection_output.strip())
        self.memory.session_memory["past_actions"].append({"step": self.step, "action": "Reflect", "result": parsed_reflection["reflection"]})
        self.memory.session_memory["short_term_memory"]["active_context"] = parsed_reflection["state"]
        self.step += 1
        return parsed_reflection

    def quick_response(self, user_input, observation):
        """Handles simple responses without full reasoning cycles."""
        context = self.memory.get_context()
        print(f"\033[1;33m{context}")
        quick_prompt = self.prompt_manager.get_quick_response_prompt(user_input, context, observation)
        print(f"\033[1;31m{quick_prompt}")
        quick_response = self.call_llm(quick_prompt)
        return quick_response

    def call_llm(self, prompt, size_flag=False):
        """Handles API call to LLaMA3."""
        bedrock_client = boto3.client("bedrock-runtime")
        if size_flag:
            model_id = "arn:aws:bedrock:us-east-1:198502499921:inference-profile/us.meta.llama3-2-90b-instruct-v1:0"
        else:
            model_id = "arn:aws:bedrock:us-east-1:198502499921:inference-profile/us.meta.llama3-3-70b-instruct-v1:0"
        
        llm_response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps({"prompt": prompt, "temperature": 0.5, "top_p": 0.9, "max_gen_len": 2048})
        )
        return json.loads(llm_response.get('body').read())['generation']