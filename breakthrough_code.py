#!usr/bin/env python

from manimlib.imports import *
import numpy as np

class Grid(VGroup):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))


class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 8,
        "columns": 14,
        "height": FRAME_Y_RADIUS * 2,
        "width": 14,
        "grid_stroke": 0.5,
        "grid_color": WHITE,
        "axis_color": RED,
        "axis_stroke": 2,
        "labels_scale": 0.25,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rows = self.rows
        columns = self.columns
        grid = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width / columns
        divisions_y = self.height / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = Text(f"{coord_point}",font="Arial",stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)


class Plot2(GraphScene):
    CONFIG = {
        "y_max" : 20,
        "y_min" : -20,
        "x_max" : 7,
        "x_min" : -7,
        "y_tick_frequency" : 5,
        "axes_color" : BLUE,
        "x_axis_label" : "$w$",
        "y_axis_label" : "$cost$",  
        "xs": np.arange(-3, 1, 0.01).tolist()
    }
    def construct(self):
        grid = ScreenGrid()
        text1 = TextMobject("The cost represents the degree of error that a model has when training itself")
        text1.to_edge(DOWN)
        text2 = TextMobject("Cost is minimized")
        text2.move_to(1.5*DOWN, 2*RIGHT)
        text3 = TextMobject("Initial cost")
        text3.move_to(UP*1, RIGHT*8)
        #text2 = TexMobject("$1/n*\sum_{i=1}^{n} {}")
        self.add(grid)
        self.setup_axes()
        graph1 = self.get_graph(lambda x : (x-1)**2, color = GREEN, x_min=-3, x_max=1)
        graph2 = self.get_graph(lambda x : (x-1)**2, color = GREEN, x_min=1, x_max=5)
        location = self.coords_to_point(-3,16)
        dot = Dot(location)
        arrow1 = Arrow(LEFT, UP)
        arrow1.move_to(UP*1, RIGHT*4.5)
        arrow2 = Arrow(LEFT, UP)
        arrow2.move_to(1*DOWN, 3.7*RIGHT)

        axes = self.axes
        # axes.x_axis.add_numbers()

        xs = self.xs

        lines = VGroup(*[
            TangentLine(
                graph1,
                inverse_interpolate(
                    self.x_min,
                    self.x_max,
                    x
                ),
                length=2,
                stroke_opacity=0.75,
            )
            for x in xs
        ])
        
        self.play(
            Write(text1),
            run_time = 2)
        self.wait(2)
        self.play(
        	ShowCreation(graph1),
            ShowCreation(graph2),
            ShowCreation(dot),
            run_time = 2
        )
        self.play(Write(text3))
        self.play(GrowArrow(arrow1))
        self.wait()
        self.play(
            MoveAlongPath(dot, graph1),
            run_time = 3
        )
        self.wait()
        self.play(GrowArrow(arrow2))
        self.wait()
        self.play(Write(text2), color=GREEN)

        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, lines)
        )

    def setup_axes(self):
        grid = ScreenGrid()
        # Add this line
        GraphScene.setup_axes(self) 
        # Parametters of labels
        #   For x
        init_label_x = -5
        end_label_x = 5
        step_x = 1
        #   For y
        init_label_y = -50
        end_label_y = 50
        step_y = 10
        # Position of labels
        #   For x
        
        self.x_axis.move_to(0.2*UP+0.45*RIGHT)
        #   For y
        self.y_axis.move_to(0.2*UP+0.45*RIGHT)
        
        # Add labels to graph
        #   For x
        self.x_axis.add_numbers(*range(
                                        init_label_x,
                                        end_label_x+step_x,
                                        step_x
                                    ))
        #   For y
        
        self.y_axis.add_numbers(*range(
                                        init_label_y,
                                        end_label_y+step_y,
                                        step_y
                                    ))
        
        #   Add Animation
        self.play(
            ShowCreation(self.x_axis),
            ShowCreation(self.y_axis)
        )

class NeuralNet(Scene):
    def construct(self):
        text = TextMobject("A column of neurons in a neural network is called a layer")
        self.play(GrowFromCenter(text))
        self.wait()
        self.play(Rotating(text))
        self.wait(3)
        self.remove(text)
        self.wait(3)


