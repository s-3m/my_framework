from views import Index, About, Contact, Catalog, CreateGenre, CreateFilm, CopyFilm

routes = {
    # '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    # '/catalog/': Catalog(),
    '/AddGenre/': CreateGenre(),
    '/AddFilm/': CreateFilm(),
    '/copy_film/': CopyFilm(),
}
