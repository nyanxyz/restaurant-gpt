from intent import get_intent_json
from review import get_review
from parking import get_parking_info_json
from search import local_search, blog_search
import util

prompt = """맛집에 대해 질문해보세요!
예시: 강남에 있는 좋은 파스타 식당 추천해주세요
예시: 낙성대 장블랑제리 후기가 궁금해요
예시: 서울대입구 하노이별에 주차가 가능한가요?
>>> """

if __name__ == '__main__':
    query = input(prompt)
    print()

    intent_json = get_intent_json(query)
    intent_type = intent_json['INTENT_TYPE']

    if intent_type == 'RESTAURANT':
        location = intent_json.get('LOCATION')
        food = intent_json.get('FOOD')

        if location is None:
            print(f'좋은 {food} 식당을 추천해드릴게요!')
            search_result = local_search(f"{food} 맛집")
        elif food is None:
            print(f'{location}에 있는 좋은 식당을 추천해드릴게요!')
            search_result = local_search(f"{location} 맛집")
        else:
            print(f'{location}에 있는 좋은 {food} 식당을 추천해드릴게요!')
            search_result = local_search(f"{location} {food} 맛집")

        for idx, item in enumerate(search_result['items']):
            category = item['category'].split('>')[1].strip()

            print(f"{idx + 1}. {item['title'].replace('<b>', '').replace('</b>', '')}")
            print(f"   {util.attach_eul_reul(category)} 판매하는 식당이에요.")
            print(f"   주소: {item['roadAddress']}")
            if item['link']:
                print(f"   사이트: {item['link']}")

    elif intent_type == 'REVIEW':
        restaurant = intent_json.get('RESTAURANT')
        location = intent_json.get('LOCATION')

        if location is None:
            print(f'{restaurant} 식당에 대한 후기를 알려드릴게요!')
            search_result = blog_search(f"{restaurant} 후기")
        else:
            print(f'{location}에 있는 {restaurant} 식당에 대한 후기를 알려드릴게요!')
            search_result = blog_search(f"{location} {restaurant} 후기")

        if len(search_result['items']) == 0:
            print(f"{restaurant} 식당에 대한 후기를 찾을 수 없어요 😢")
            exit()

        for idx, item in enumerate(search_result['items']):
            blog_post = util.get_url_content(item['link'])

            if blog_post is None:
                continue

            content = f'"""{blog_post}"""'

            review = get_review(content)
            if review.startswith("'") or review.startswith('"'):
                review = review[1:]
            if review.endswith("'") or review.endswith('"'):
                review = review[:-1]

            print(f"{idx + 1}. {review}")
            print(f"   출처: {item['link']}")

    elif intent_type == 'PARKING':
        restaurant = intent_json.get('RESTAURANT')
        location = intent_json.get('LOCATION')

        if location is None:
            print(f'{restaurant} 식당에 대한 주차 정보를 알려드릴게요!')
            search_result = blog_search(f"{restaurant} 주차")
        else:
            print(f'{location}에 있는 {restaurant} 식당에 대한 주차 정보를 알려드릴게요!')
            search_result = blog_search(f"{location} {restaurant} 주차")

        info = None
        for idx, item in enumerate(search_result['items']):
            blog_post = util.get_url_content(item['link'])

            if blog_post is None:
                continue

            content = f'"""{blog_post}"""'

            parking_info = get_parking_info_json(content)
            if parking_info['available'] != 'unknown':
                if parking_info['available'] == 'true':
                    print(f"{restaurant} 식당에는 주차가 가능합니다.")
                else:
                    print(f"{restaurant} 식당에는 주차가 불가능합니다.")

                info = parking_info.get('info')
                info = info.replace('주차 :', ' ')
                info = info.strip()

                if info:
                    print(f"   💡 {info}")
                print(f"   출처: {item['link']}")
                break

        if info is None:
            print(f"{restaurant} 식당에 대한 주차 정보를 찾을 수 없어요 😢")
            exit()