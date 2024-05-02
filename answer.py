from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts.few_shot import FewShotPromptTemplate
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it")

examples=[
        {"問題": "外頭現在 32 度，我應該把室內溫度設定為多少比較好？", "答案": "根據基本原則，室內外的溫差最好間距在 5 度，所以室內溫度應該設定為 27 度。"},
        {"問題": "今天外面 30 度，室內溫度應該調到多少？", "答案": "室內溫度應該設定為 25 度，這樣可以保持室內外溫差在 5 度左右。"}
]

example_prompt = PromptTemplate.from_template(
    template = "以下是一些室內外溫度設定的問題和解答範例:\n\n問題: {問題}\n答案: {答案}\n",
)

prompt = FewShotPromptTemplate(
    examples = examples,
    example_prompt = example_prompt,
    suffix = "Question: {prompt}",
    input_variables=["prompt"],
)
print(llm.invoke(prompt.format(prompt="外頭現在 27 度，好熱，我應該把室內溫度調到多少？")))
