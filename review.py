from gpt import get_gpt_response


def get_review(post):
    system_prompt = """
        You will receive a blog post enclosed within triple quotes, detailing a review of a specific restaurant.
        
        Your task is to provide a concise one-sentence summary of the blog post, ideally around 30 words in length.
        The summary should capture the essence of the review, focusing on the main points or overall impression of the restaurant.
        Please ensure your summary ends with '라는 후기입니다.'
        
        For example, if the review suggests a clean and orderly atmosphere conducive to dining,
        your summary could be '깔끔하고 정갈한 분위기에서 식사하기 좋은 곳이라는 후기입니다.'
        """

    return get_gpt_response(system_prompt, post, max_tokens=128)
