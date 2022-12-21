import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id, fields=["bdate"])
    ages = []
    for friend in friends.items:
        if "bdate" in friend:
            bdate = friend["bdate"].split(".")
            if len(bdate) == 3:
                try:
                    age = dt.datetime.now().year - int(bdate[2])
                    ages.append(age)
                except ValueError:
                    pass
    if len(ages) > 0:
        return statistics.median(ages)
    else:
        return None
