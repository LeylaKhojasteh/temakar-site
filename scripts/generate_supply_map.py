"""ساخت نقشهٔ سادهٔ اروپا تا خاورمیانه برای بخش «مسیر تأمین».

دادهٔ منبع: Natural Earth 110m land (public domain، naturalearthdata.com).
فایل خام در مخزن نگه داشته نمی‌شود؛ برای بازتولید:

    curl -o .taste-skill/land.geojson \
      https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson

"""

import json
import math
from pathlib import Path

SOURCE = Path(".taste-skill/land.geojson")
TARGET = Path("static/img/supply-map.svg")

# پنجرهٔ جغرافیایی: از اقیانوس اطلس تا آسیای مرکزی
LON_MIN, LON_MAX = -8.0, 72.0
LAT_MIN, LAT_MAX = 20.0, 54.0
STANDARD_PARALLEL = math.radians(38.0)
WIDTH = 1200


def project(lon: float, lat: float) -> tuple[float, float]:
    x = (lon - LON_MIN) * math.cos(STANDARD_PARALLEL)
    y = LAT_MAX - lat
    return x, y


def simplify(points: list[tuple[float, float]], tolerance: float) -> list[tuple[float, float]]:
    if len(points) < 3:
        return points

    def rdp(pts: list[tuple[float, float]], eps: float) -> list[tuple[float, float]]:
        if len(pts) < 3:
            return pts
        start, end = pts[0], pts[-1]
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy)
        index, best = -1, 0.0
        for i in range(1, len(pts) - 1):
            if length == 0:
                dist = math.hypot(pts[i][0] - start[0], pts[i][1] - start[1])
            else:
                dist = abs(dy * pts[i][0] - dx * pts[i][1] + end[0] * start[1] - end[1] * start[0]) / length
            if dist > best:
                index, best = i, dist
        if best > eps:
            return rdp(pts[: index + 1], eps)[:-1] + rdp(pts[index:], eps)
        return [start, end]

    return rdp(points, tolerance)


def path_for(ring: list[list[float]]) -> str:
    pts = [project(lon, lat) for lon, lat in ring]
    pts = simplify(pts, tolerance=0.06)
    if len(pts) < 3:
        return ""
    step = "M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in [pts[0]]) + " L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"
    return step


def ring_visible(ring: list[list[float]]) -> bool:
    margin = 4.0
    return any(
        LON_MIN - margin <= lon <= LON_MAX + margin and LAT_MIN - margin <= lat <= LAT_MAX + margin
        for lon, lat in ring
    )


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    paths: list[str] = []

    for feature in data["features"]:
        geometry = feature.get("geometry") or {}
        coordinates = geometry.get("coordinates") or []
        if geometry.get("type") == "Polygon":
            polygons = [coordinates]
        elif geometry.get("type") == "MultiPolygon":
            polygons = coordinates
        else:
            continue
        for polygon in polygons:
            for ring in polygon:
                if ring_visible(ring):
                    path = path_for(ring)
                    if path:
                        paths.append(path)

    width_units = (LON_MAX - LON_MIN) * math.cos(STANDARD_PARALLEL)
    scale = WIDTH / width_units
    height = round((LAT_MAX - LAT_MIN) * scale)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" height="{height}" role="img" aria-label="Map of Europe, North Africa and the Middle East">',
        '<rect width="100%" height="100%" fill="#0b2336"/>',
        '<g fill="#1d3b51" stroke="#4f6e86" stroke-width="1.2" stroke-linejoin="round">',
        *(f'<path d="{path}"/>' for path in paths),
        "</g>",
        "</svg>",
    ]
    TARGET.write_text("\n".join(svg), encoding="utf-8")

    def point(lon: float, lat: float) -> tuple[float, float]:
        x, y = project(lon, lat)
        return round(x * scale, 1), round(y * scale, 1)

    print(f"viewBox: 0 0 {WIDTH} {height}")
    print("europe:", [point(lon, lat) for lon, lat in ((4.0, 50.0), (9.0, 51.0), (15.0, 48.0))])
    print("tehran:", point(51.4, 35.7))
    print("nodes:", [point(lon, lat) for lon, lat in ((62.0, 38.0), (58.0, 33.0), (63.0, 30.0))])
    print(f"paths: {len(paths)}; size: {TARGET.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
