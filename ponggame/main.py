from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.1
            ball.velocity_y *= 1.1

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce off paddles
        if self.player1:
            self.player1.bounce_ball(self.ball)
        if self.player2:
            self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went off a side to score point?
        if self.ball.x < self.x:
            if self.player2:
                self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            if self.player1:
                self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 2:
            if self.player1:
                self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 2:
            if self.player2:
                self.player2.center_y = touch.y

    def on_size(self, *args):
        if not self.ball:
            self.ball = PongBall()
        self.serve_ball()

        if not self.player1:
            self.player1 = PongPaddle()
            self.add_widget(self.player1)
        self.player1.center_x = self.x + 50
        self.player1.center_y = self.height / 2

        if not self.player2:
            self.player2 = PongPaddle()
            self.add_widget(self.player2)
        self.player2.center_x = self.width - 50
        self.player2.center_y = self.height / 2

        self.ball.center = self.center

class PongApp(App):
    def on_start(self):
        game = PongGame()
        game.width = 800
        game.height = 600
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
