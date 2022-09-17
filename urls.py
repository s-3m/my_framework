from views import Index, About, Contact, Catalog, CreateGenre, CreateFilm

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    '/catalog/': Catalog(),
    '/AddGenre/': CreateGenre(),
    '/AddFilm/': CreateFilm()
}
