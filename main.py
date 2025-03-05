from graphics import Window, Line, Point


def main():
    win = Window(800, 600)
    l = Line(Point(50,50), Point(50,400))
    r = Line(Point(400,50), Point(400,400))
    t = Line(Point(50,50), Point(400,50))
    b = Line(Point(50,400), Point(400,400))
    win.draw_line(l, "red")
    win.draw_line(r, "blue")
    win.draw_line(t, "green")
    win.draw_line(b, "purple")
    win.wait_for_close()


main()