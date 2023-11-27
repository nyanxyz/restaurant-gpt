from gpt import get_gpt_response
import json


def get_parking_info(post):
    system_prompt = """
        You will receive a blog post enclosed within triple quotes, which may include information about parking at a specific restaurant.
        
        Your task is to determine whether parking is available and, if there are any sentences related to parking information, extract them.
        Focus on identifying key details about parking facilities, such as location, capacity, or any special instructions provided in the review.
        
        Provide output in JSON format as follows:
        
        {
            "available": "true" or "false" or "unknown",
            "info": {one-sentence, under 30 words} // optional
        }
        """

    return get_gpt_response(system_prompt, post, max_tokens=128)


def get_parking_info_json(post):
    while True:
        parking_info_json_str = get_parking_info(post)

        try:
            data = json.loads(parking_info_json_str)
        except json.JSONDecodeError:
            print("Error: 문자열이 올바른 JSON 형식이 아닙니다. (get_parking_info_json)")
            continue
        else:
            return data
