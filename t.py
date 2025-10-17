from data import Films

films = Films()

def get_films_by_chunk(items: tuple[str]) -> list: 

    """The function is used to divide the original data into chunks of 500 items to process vie the DeepSeek"""

    movies = [
    films.GET_ONE_FROM_A_LIST_OF_FILMS[i:i+500] for i in range(0, len(films.GET_ONE_FROM_A_LIST_OF_FILMS), 500)
    ]

    return movies
