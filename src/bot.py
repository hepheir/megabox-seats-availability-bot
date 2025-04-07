import collections
import datetime
import os
import discord
import megabox


TARGET_MOVIE_NO = "25008000"  # 진격거 완결편 극장판
TARGET_THEATER_ID = 1351  # 코엑스 메가박스
TARGET_DATES = [
    datetime.date(2025, 4, 11),  # 금
    datetime.date(2025, 4, 12),  # 토
    datetime.date(2025, 4, 13),  # 일
    datetime.date(2025, 4, 19),  # 토
    datetime.date(2025, 4, 20),  # 일
]


def is_what_we_are_looking_for(movie: megabox.MovieForm) -> bool:
    if not movie.is_2d_mx4d:
        return False
    if not movie.branch_id == TARGET_THEATER_ID:
        return False
    available_seats = max(movie.rest_seat_count - 4, 0)  # 장애인석 제외
    if available_seats < 3:
        return False
    return True


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = 1358260652497440909  # 허밍 디스코드 진격거 쓰레드

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    channel = client.get_channel(CHANNEL_ID)
    lines = collections.deque()
    for date in TARGET_DATES:
        print(f'Scanning for {date}...')
        for movie in megabox.select_bokd_list(TARGET_MOVIE_NO, date).movie_form_list:
            if is_what_we_are_looking_for(movie):
                lines.append(f'- {movie.play_date}({"월화수목금토일"[date.weekday()]}) {movie.play_start_time}-{movie.play_end_time} : `{movie.rest_seat_count}`석 남아있어!')
    if lines:
        lines.appendleft(f'삐용삐용!!! 우와아앗...!! 코엑스에 자리난 것 같아!')
        lines.append(f'')
        lines.append(f'서두르는게 좋을 것 같아, 행운을 빌어!')
        lines.append(f'(잔여석 중 약 4석은 장애인 전용석이라는 점에 유의해!)')
        await channel.send('\n'.join(lines))
    else:
        lines.append(f'아직까진 코엑스에 자리가 없는 것 같아... ㅠㅠ')
        # await channel.send('\n'.join(lines))
    await client.close()

client.run(token=TOKEN)
