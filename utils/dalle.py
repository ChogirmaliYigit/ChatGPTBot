import requests


def generate_image(openai_key, model, prompt, num=2):
  url = 'https://api.openai.com/v1/images/generations'
  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai_key}'
  }
  data = {
    'model': f'{model}', # image-alpha-001
    'prompt': f'{prompt}',
    'num_images': num
  }

  response = requests.post(url, headers=headers, json=data)
  if response.status_code == 200:
    result = response.json()
    return result
  else:
    print(response.content)
    return 'Xatolik'
