from views import Index, About, Contact, Catalog

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    '/catalog/': Catalog()
}
