from gpt import get_gpt_response
import json


def classify_intent(query):
    system_prompt = """
    You will be provided with user's query about a restaurant.
    Classify each query into a category and extract the values.

    The categories and values to extract are:
    - INTENT_TYPE: RESTAURANT
        - The user wants to know about good restaurants. (ex: 강남 맛집, 파스타 식당)
        - VALUE: LOCATION > location of the restaurant (ex: 강남)
        - VALUE: FOOD > food that the restaurant serves (ex: 파스타)
    - INTENT_TYPE: REVIEW
        - The user wants to know about reviews of a specific restaurant. (ex: 브레드 앤 브루어스 후기)
        - VALUE: RESTAURANT > name of the restaurant (ex: 브레드 앤 브루어스)
        - VALUE: LOCATION > location of the restaurant (ex: 강남)
    - INTENT_TYPE: PARKING
        - The user wants to know about parking information of a specific restaurant. (ex: 브레드 앤 브루어스 주차장)
        - VALUE: RESTAURANT > name of the restaurant (ex: 브레드 앤 브루어스)
        - VALUE: LOCATION > location of the restaurant (ex: 강남)

    Provide output in JSON format as follows:

    {
        "INTENT_TYPE": {category},
        "LOCATION": {location}, // optional
        "FOOD": {food}, // optional
        "RESTAURANT": {restaurant} // optional
    }
    """

    return get_gpt_response(system_prompt, query)


def get_intent_json(query):
    while True:
        intent_json_str = classify_intent(query)

        try:
            data = json.loads(intent_json_str)
        except json.JSONDecodeError:
            print("Error: 문자열이 올바른 JSON 형식이 아닙니다. (get_intent_json)")
            continue
        else:
            return data