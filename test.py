import rumps

class AT(rumps.App):
    def __init__(self):
        super(AT, self).__init__("AT")
        self.menu = ["Show adistools", None]


    @rumps.clicked("Show adistools")
    def sayhi(self, _):
        rumps.notification("adistools", None, "hi!!1")

if __name__ == "__main__":
    at=AT()
    at.run()