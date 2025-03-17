from pynput import keyboard
import openai
import pyperclip

openai.api_key = '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'

def send_prompt_to_chatgpt(prompt):
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You will answer concisely and succinctly, your answer should be human-like and should not show arbitrary working out, students will have your answer directly in a document and it should not look out of the ordinary."},
        {"role": "user", "content": prompt}
    ]
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=150  
    )
    
    return response.choices[0].message['content']

captured_keys = []
ctrl_pressed = False
shift_pressed = False

def on_press(key):
    global captured_keys, ctrl_pressed, shift_pressed
    try:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            ctrl_pressed = True
        elif key == keyboard.Key.shift:
            shift_pressed = True
        elif key == keyboard.Key.space and ctrl_pressed and shift_pressed:
            prompt = ''.join(captured_keys)
            if prompt.strip():
                answer = send_prompt_to_chatgpt(prompt)
                pyperclip.copy(answer)
                captured_keys = []  #
        elif hasattr(key, 'char') and key.char:
            captured_keys.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            captured_keys.append(' ')

def on_release(key):
    global ctrl_pressed, shift_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False
    elif key == keyboard.Key.shift:
        shift_pressed = False
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
