import datetime
import os
import time
import typing
import discord
import megabox


TIMEZONE = datetime.timezone(datetime.timedelta(hours=9), 'KST')

DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID_WARN = 1358260652497440909  # 찾으면 알림 보낼 채널 (허밍 디스코드 진격거 쓰레드)
DISCORD_CHANNEL_ID_INFO = 1359011032542085322  # 못찾아도 결과 보낼 채널

TARGET_MOVIE_NO = "25008000"  # 진격거 완결편 극장판
TARGET_THEATER_ID = 1351  # 코엑스 메가박스
TARGET_REQUIRED_SEATS = 3 # 우리에게 필요한 최소 좌석 수
TARGET_DATES = [
    datetime.date(2025, 4, 11),  # 금
    datetime.date(2025, 4, 12),  # 토
    datetime.date(2025, 4, 13),  # 일
    datetime.date(2025, 4, 19),  # 토
    datetime.date(2025, 4, 20),  # 일
]


intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    movies = find_all_movies(movie_no=TARGET_MOVIE_NO)
    movies = list(filter(is_what_we_are_looking_for, movies))

    if movies:
        message = (
            f'삐용삐용!!! 우와아앗...!! 코엑스에 자리난 것 같아!\n'
            +'\n'.join(map(movie_to_string, movies))+'\n'+
            f'\n'
            f'서두르는게 좋을 것 같아, 행운을 빌어!\n'
            f'(잔여석 중 약 4석은 장애인 전용석이라는 점에 유의해!)\n'
        )
        print(message)
        await client.get_channel(DISCORD_CHANNEL_ID_INFO).send(message)
        await client.get_channel(DISCORD_CHANNEL_ID_WARN).send(message)
    else:
        message = (
            f'아직까진 코엑스에 자리가 없는 것 같아... ㅠㅠ'
            f' ({datetime.datetime.now().astimezone(TIMEZONE).strftime("%m.%d %H:%M")})'
        )
        print(message)
        await client.get_channel(DISCORD_CHANNEL_ID_INFO).send(message)
    await client.close()


def find_all_movies(movie_no: str) -> typing.List[megabox.MovieForm]:
    founds = []
    for date in TARGET_DATES:
        founds.extend(megabox.select_bokd_list(movie_no, date).movie_form_list)
    return founds


def is_what_we_are_looking_for(movie: megabox.MovieForm) -> bool:
    if not movie.is_2d_mx4d:
        return False
    if not movie.branch_id == TARGET_THEATER_ID:
        return False
    available_seats = max(movie.rest_seat_count - 4, 0)  # 장애인석 제외
    if available_seats < TARGET_REQUIRED_SEATS:
        return False
    return True


def movie_to_string(movie: megabox.MovieForm) -> str:
    return f'- {movie.play_date}({"월화수목금토일"[movie.play_date.weekday()]}) {movie.play_start_time}-{movie.play_end_time} : `{movie.rest_seat_count}`석 남아있어!'


try:
    client.run(token=DISCORD_TOKEN)
except Exception:
    time.sleep(10)
    client.run(token=DISCORD_TOKEN)
