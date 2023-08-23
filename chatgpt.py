import os
import openai
openai.api_key = "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"



def chatWithGPT(prompt):
  completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  # model="gpt-4-0314",
  messages=[
  {"role": "user", "content": prompt}
  ]
  )
  return print(completion.choices[0].message.content)

chatWithGPT("Привет! могу ли я общаться с тобой, как с живым человеком?")