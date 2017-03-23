class Movie:
    '''
    This class represents a movie reference. It contains fields describing
    the movie, such as: title, description, poster image and a link
    to movie's trailer
    '''
    def __init__(self, title, desc, img, trailer):
        self.title = title
        self.desc = desc
        self.img = img
        self.trailer = trailer


def create_list():
    '''
    This function returns a list of Movie class instances populated by me.
    '''
    movies = []
    movies.append(
        Movie(
            "Pulp Fiction (1994)",
            "The lives of two mob hit men, a boxer, a gangster's wife, "
            "and a pair of diner bandits intertwine in four tales of violence"
            " and redemption.",
            "https://images-na.ssl-images-amazon.com/images/M/MV5BMTkxMTA5OTAzMl5BMl5BanBnXkFtZTgwNjA5MDc3NjE@._V1_SY1000_CR0,0,673,1000_AL_.jpg",  # NOQA
            "https://www.youtube.com/watch?v=s7EdQ4FqbhY"
        )
    )
    movies.append(
        Movie(
            "Paprika (2006)",
            "When a machine that allows therapists to enter their "
            "patients' dreams is stolen, all Hell breaks loose. "
            "Only a young female therapist, Paprika, can stop it.",
            "https://images-na.ssl-images-amazon.com/images/M/MV5BNDliMTMxOWEtODM3Yi00N2QwLTg4YTAtNTE5YzBlNTA2NjhlXkEyXkFqcGdeQXVyNjE5MjUyOTM@._V1_SY1000_CR0,0,666,1000_AL_.jpg",  # NOQA
            "https://www.youtube.com/watch?v=jJzEW_eE1G0"
        )
    )
    movies.append(
        Movie(
            "Blade Runner (1982)",
            "A blade runner must pursue and try to terminate four "
            "replicants who stole a ship in space and have returned "
            "to Earth to find their creator.",
            "https://images-na.ssl-images-amazon.com/images/M/"
            "MV5BZWZlYmEyYTItNGRjYy00ZmMxLWEzMWItM2Q2NjZlNTMwMjQ3XkEyXkFqcGdeQXVyNDYyMDk5MTU@._V1_SY1000_CR0,0,665,1000_AL_.jpg",  # NOQA
            "https://www.youtube.com/watch?v=eogpIG53Cis"
        )
    )
    movies.append(
        Movie(
            "Eternal Sunshine of the Spotless Mind (2004)",
            "When their relationship turns sour, a couple undergoes "
            "a procedure to have each other erased from their memories. "
            "But it is only through the process of loss that they "
            "discover what they had to begin with.",
            "https://images-na.ssl-images-amazon.com/images/M/MV5BMTY4NzcwODg3Nl5BMl5BanBnXkFtZTcwNTEwOTMyMw@@._V1_SY1000_CR0,0,674,1000_AL_.jpg",  # NOQA
            "https://www.youtube.com/watch?v=yE-f1alkq9I"
        )
    )
    return movies
