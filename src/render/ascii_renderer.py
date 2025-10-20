class AsciiRenderer:
    def __init__(
            self,
            canvas_res: tuple
    ) -> None:
        self.canvas_plane_x = canvas_res[0]
        self.canvas_plane_y = canvas_res[1] 

        self.asciis = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]

    def _luminance_to_ascii(
            self,
            luminance: float
    ) -> str:
        idx = int(luminance * (len(self.asciis) - 1))
        return self.asciis[idx]

    def render(
            self,
            points: dict
    ) -> str:
        out = ""

        for y in range(self.canvas_plane_y):
            row = []
            for x in range(self.canvas_plane_x):
                luminance, _, _ = points.get((x, y), (0.0, 0.0, 0.0))
                row.append(self._luminance_to_ascii(luminance))
            out += "".join(row)+ "\n"

        return out
