from utils.chat_history import ChatHistory
from services.search import local_search, blog_search
from utils.text_utils import attach_eul_reul, get_url_content
from models.review import get_review
from models.parking import get_parking_info_json


class RestaurantController:
    def __init__(self):
        self.chat_history = ChatHistory()

    def log(self, message="", end="\n"):
        self.chat_history.log(message, end)

    def find_restaurants(self, location, food):
        if location is None:
            message = f"좋은 {food} 식당을 추천해드릴게요!"
            search_query = f"{food} 맛집"
        elif food is None:
            message = f"{location}에 있는 좋은 식당을 추천해드릴게요!"
            search_query = f"{location} 맛집"
        else:
            message = f"{location}에 있는 좋은 {food} 식당을 추천해드릴게요!"
            search_query = f"{location} {food} 맛집"

        self.log(message)
        search_result = local_search(search_query)

        for idx, item in enumerate(search_result["items"]):
            category = item["category"].split(">")[1].strip()

            self.chat_history.log(
                f"""{idx + 1}. {item['title'].replace('<b>', '').replace('</b>', '')}
    {attach_eul_reul(category)} 판매하는 식당이에요.
    주소: {item['roadAddress']}"""
            )
            if item["link"]:
                self.log(f"    사이트: {item['link']}")

    def find_reviews(self, restaurant, location):
        if location is None:
            message = f"{restaurant} 식당에 대한 후기를 알려드릴게요!"
            search_query = f"{restaurant} 후기"
        else:
            message = f"{location}에 있는 {restaurant} 식당에 대한 후기를 알려드릴게요!"
            search_query = f"{location} {restaurant} 후기"

        self.log(message)
        search_result = blog_search(search_query)

        if len(search_result["items"]) == 0:
            self.log(f"{restaurant} 식당에 대한 후기를 찾을 수 없어요 😢")
            exit()

        for idx, item in enumerate(search_result["items"]):
            blog_post = get_url_content(item["link"])

            if blog_post is None:
                continue

            content = f'"""{blog_post}"""'

            stream = get_review(content)

            self.log(f"{idx + 1}. ", end="")
            for part in stream:
                self.log(part.choices[0].delta.content or "", end="")
            self.log()
            self.log(f"   출처: {item['link']}")

    def find_parking_info(self, restaurant, location):
        if location is None:
            message = f"{restaurant} 식당에 대한 주차 정보를 알려드릴게요!"
            search_query = f"{restaurant} 주차"
        else:
            message = f"{location}에 있는 {restaurant} 식당에 대한 주차 정보를 알려드릴게요!"
            search_query = f"{location} {restaurant} 주차"

        self.log(message)
        search_result = blog_search(search_query)

        info = None
        for idx, item in enumerate(search_result["items"]):
            blog_post = get_url_content(item["link"])

            if blog_post is None:
                continue

            content = f'"""{blog_post}"""'

            parking_info = get_parking_info_json(content)
            if parking_info["available"] != "unknown":
                if parking_info["available"] == "true":
                    self.log(f"{restaurant} 식당에는 주차가 가능합니다.")
                else:
                    self.log(f"{restaurant} 식당에는 주차가 불가능합니다.")

                info = parking_info.get("info")
                info = info.replace("주차 :", " ")
                info = info.strip()

                if info:
                    self.log(f"   💡 {info}")
                self.log(f"   출처: {item['link']}")
                break

        if info is None:
            self.log(f"{restaurant} 식당에 대한 주차 정보를 찾을 수 없어요 😢")
