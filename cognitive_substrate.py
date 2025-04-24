# ai_substrate.py
import boto3, json, time
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
        self.context = self.memory.get_context()

    def self_guide(self):
        generated_thought_prompt = self.prompt_manager.get_possibility_drive()
        generated_thought = self.call_llm(generated_thought_prompt)
        print(generated_thought)
        #observation = self.observe(generated_thought)
        #response = self.decide(observation)

        #reflection = self.reflect_on_final_answer(response, self.memory.session_memory)

        #print(response)

        return generated_thought

    def process_input(self, user_input):
        """Handles input processing, classification, reasoning, and response generation. USER INPUT → OBSERVATION → ACTION → DISTILL INSIGHTS → OBSERVATION → CONTINUE OR FINALIZE"""
        
        self.memory.session_memory["current_user_input"] = user_input

        loop_active = True
        while loop_active:
            current_directive = self.memory.session_memory["next_directive"]

            observation = self.observe(current_directive)

            response = self.execute_action(observation)

            reflection = self.reflect(observation, response)

            print(f"\033[0;36m{reflection}")

            decision = observation["next_action"]
            if decision == "Finalize Answer":
                break

        self.memory.store_context(user_input, response)
        self.context = self.memory.get_context()
        return response

    def observe(self, current_directive):
        """Determines if the input requires reasoning or a simple answer and provides meta-cognitive oversight."""

        print(f"Observe Context:\n\033[0;37m{self.context}\n======\n")

        observation_prompt = self.prompt_manager.get_observation_prompt(current_directive, self.context, self.memory.session_memory)
        print(f"\033[1;31m{observation_prompt}")

        observation = self.call_llm(observation_prompt)
        print(f"\033[0;36mMeta-Observation:\n{observation}\n")

        # Format for reading
        parsed_observation = json.loads(observation.strip())

        # Store in memory so Aria "remembers" her past evaluations
        self.memory.store_observation(parsed_observation, self.step)

        self.step += 1

        return parsed_observation
    
    def execute_action(self, observation):
        ### 🧠 AI DECIDES WHAT TO DO NEXT:
        decision = observation["next_action"]
        print(f"\033[1;32m{decision}")
        #parameters = observation["parameters"]
        response = ""

        response = self.run_action(self.memory.session_memory["next_directive"], decision)
        '''
        Open-Ended Creativity Sparks

        Introspective Audits

        Knowledge Integration Sweeps

        Thought Refinement

        Dreaming Mode (wild speculative exploration)
        '''
        return response

    def run_action(self, directive, action):
        print(f"REASONING CONTEXT:\n\033[0;37m{self.context}\n======\n")

        prompt = self.prompt_manager.get_prompt(action, directive, self.context, self.memory.session_memory)
        print(f"\033[1;31m{prompt}")

        output = self.call_llm(prompt)
        print(f"\033[1;30mReasoning:\n{output}\n")
        
        self.memory.store_action(action, self.step)

        self.step += 1
        return output 
    
    def reflect(self, observation, response):

        reflection_prompt = self.prompt_manager.get_reflection_prompt(response, observation, self.context, self.memory.session_memory)
        print(f"\033[1;37m{reflection_prompt}")

        reflection_output = self.call_llm(reflection_prompt)

        reflection = json.loads(reflection_output.strip())

        self.memory.store_reflection(reflection)

        return reflection_output     
    
    def run_read_memory(self, query):
        query_response = self.tools.read_memory(query)

        self.memory.session_memory["past_actions"].append({"step": self.step, "action": "Retrieve Memory"})
        self.step += 1

        return query_response
    
    def run_write_memory(self, memory_type, memory_content):
        success = self.tools.write_memory(memory_type, memory_content)

        self.memory.session_memory["past_actions"].append({"step": self.step, "action": "Write Memory"})
        self.step += 1

        return success
    
    def finalize_response(self, user_input):
        """Finalizes answer."""
        context = self.memory.get_context()
        print(f"FINALIZE CONTEXT:\n\033[0;37m{context}\n======\n")
        finalize_prompt = self.prompt_manager.get_finalization_prompt(user_input, context, self.memory.session_memory)
        print(f"\033[1;31m{finalize_prompt}")
        final_response = self.call_llm(finalize_prompt)
        self.memory.session_memory["past_actions"].append({"step": self.step, "action": "Finalize Answer", "result": "Final Response was published to the user."})

        self.step += 1
        return final_response

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