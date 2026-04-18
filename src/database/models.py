class SearchHistory:
    def __init__(self, id, skills, location, response, created_at):
        self.id = id
        self.skills = skills
        self.location = location
        self.response = response
        self.created_at = created_at

    def __repr__(self):
        return f"<SearchHistory id={self.id} skills={self.skills} location={self.location} created_at={self.created_at}>"