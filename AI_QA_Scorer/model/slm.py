# from llama_cpp import Llama
import pathlib
import requests

class Grade:

    def grade(self, question, answer, keywords_hit, sim_score, must_include, synonyms, misconceptions, numeric_rules):
        
        parent_dir = pathlib.Path(__file__).parent.parent
        model_path = parent_dir / 'fine_tuned_model'
        model_path_file = model_path / 'gemma-3-1b-it.Q4_K_M.gguf'

        # Download the model
        # model_name = "Qwen/Qwen3-0.6B-GGUF"

        # llm = Llama.from_pretrained(
        # repo_id=model_name,
        # n_gpu_layers=-1,
        # filename="*q8_0.gguf",
        # # filename="Qwen3-4B-Q8_0.gguf",
        # # filename='qwen2.5-0.5b-instruct-fp16.gguf',
        # local_dir=model_path,
        # verbose=False,
        # )

        # quit()

        # LOAD model gguf from local dir
        # print(model_path)
        # quit()
        # llm = Llama(
        #         model_path=str(model_path_file),
        #         n_gpu_layers=-1,
        #         local_files_only=True,
        #         chat_format="chatml",
        #         n_ctx=2048
        #         )
               
        # Define the messages for the chat completion, including the system and user roles
        # messages = [
        # {"role": "system", "content": "You are a strict but kind answer grader for 8-13 year-olds. Return the score and verdict based on student answer accuracy. Return JSON response."},
        # {"role": "user", "content": f"""
        # QUESTION:
        # {question}
        # RUBRIC:
        # - Must include: {must_include}
        # - Acceptable synonyms: {synonyms}
        # - Misconceptions to penalize: {misconceptions}
        # - Numeric rules: {numeric_rules}
        # HEURISTICS:
        # - Keyword hits: {keywords_hit}%
        # - Embedding similarity (0-1): {sim_score}
        # STUDENT ANSWER:
        # {answer}
        # RESPONSE FORMAT:
        # "score": "integer between 0 to 5", 
        # "verdict": "correct|partial|incorrect",
        # "feedback": "≤140 chars, kind, 1-step tip",
        # "missing_points": "..."
        # """
        # }
        # ]
        
        # response_format = {
        # "type": "json_object",
        # "schema": {
        #     "type": "object",
        #     "properties": {
        #         "score": {"type": "integer", "description": "0-5, integer, based on the student answer"},
        #         "verdict": {"type": "string", "description": "Student Answer verdict: correct|incorrect|partial"},
        #         "feedback": {"type": "string", "description": "≤140 chars, kind, 1-step tip"},
        #         "missing_points": {"type": "string", "description": "tell any missed points in answer based on rubric"}
        #         },
        #     "required": ["score", "verdict", "feedback", "missing_points"],
        #     }
        # }
        
        # output = llm.create_chat_completion(
        # messages=messages,
        # response_format=response_format,
        # max_tokens=None,
        # temperature=0.9
        # )

        messages = "You are a strict but kind answer grader for 8-13 year-olds. Return the score and verdict based on student answer accuracy. Question: " + question + " Answer: " + answer;

        # Set URL
        url = "https://nitinplays247-google-gemma-api.hf.space/generate"

        # 2. Set the prompt query parameter
        query_params = {"prompt": messages}
        
        # 3. Send the POST request
        response = requests.post(url, params=query_params)
        
        # 4. Parse and print the JSON response
        # data = response.json()
        
        # return output['choices'][0]['message']['content']
        return response

# Run
# example = Grade()       
# out = example.grade('what is the chemical formula for water', 'H2O2', 75, 0.86, 'H2O', {'h2o', 'H2o'}, 'Answer should be H2O without a zero in it', 'none')
# out = example.grade('what is the chemical formula for benzene?', 'c6h6', 75, 0.76, 'C6H6', 'c6h6', 'Use capital letters for formulas', 'none')
# print(out)
