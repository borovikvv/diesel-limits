"""
Подготовка чистой геометрии России для D3-карты:
- Берём только главный полигон каждого региона (без сотен островов)
- Корректно обрабатываем 180-й меридиан (Чукотка, Якутия)
- Сдвигаем Чукотку для компактности (без полос)
- Упрощаем до разумной точности
"""
import json
import os
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely.affinity import translate
from shapely.ops import unary_union

IN_PATH  = "/home/z/my-project/data/russia_regions_simplified.geojson"
OUT_PATH = "/home/z/my-project/data/russia_clean.geojson"

def unwrap_antimeridian(geom):
    """Корректно обрабатывает полигоны, пересекающие 180-й меридиан.
    Полигоны с lon > 180 сдвигаем на -360, чтобы они были в диапазоне [-180, 0].
    """
    if geom.geom_type == "Polygon":
        coords = list(geom.exterior.coords)
        # Если есть точки с lon > 180, сдвигаем весь полигон
        if any(c[0] > 180 for c in coords):
            new_coords = [(c[0] - 360, c[1]) for c in coords]
            return Polygon(new_coords, [list(h.coords) for h in geom.interiors])
        return geom
    elif geom.geom_type == "MultiPolygon":
        polys = []
        for p in geom.geoms:
            coords = list(p.exterior.coords)
            if any(c[0] > 180 for c in coords):
                new_coords = [(c[0] - 360, c[1]) for c in coords]
                polys.append(Polygon(new_coords, [list(h.coords) for h in p.interiors]))
            else:
                polys.append(p)
        return MultiPolygon(polys)
    return geom

def main():
    with open(IN_PATH) as f:
        gj = json.load(f)

    new_features = []
    for ft in gj["features"]:
        name = ft["properties"]["region"]
        try:
            geom = shape(ft["geometry"])
        except Exception as e:
            print(f"⚠ {name}: не удалось разобрать геометрию: {e}")
            continue

        # 1. Валидация
        try:
            geom = make_valid(geom)
        except Exception:
            pass

        # 2. Анти-меридиан
        geom = unwrap_antimeridian(geom)

        # 3. Берём только самый большой полигон (без островов)
        if geom.geom_type == "MultiPolygon":
            biggest = max(geom.geoms, key=lambda p: p.area)
            geom = biggest
        elif geom.geom_type == "GeometryCollection":
            polys = [g for g in geom.geoms if g.geom_type == "Polygon"]
            if polys:
                geom = max(polys, key=lambda p: p.area)
            else:
                continue
        elif geom.geom_type != "Polygon":
            continue

        # 4. Упрощение
        geom = geom.simplify(0.05, preserve_topology=True)

        # 5. Фильтр микро-полигонов (< 0.01 deg²)
        if geom.area < 0.01:
            print(f"⚠ {name}: слишком маленький полигон ({geom.area:.4f} deg²), пропускаем")
            continue

        new_features.append({
            "type": "Feature",
            "properties": {"region": name},
            "geometry": mapping(geom),
        })
        print(f"✓ {name}: {geom.area:.2f} deg²")

    out = {"type": "FeatureCollection", "features": new_features}
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, ensure_ascii=False)

    size_kb = os.path.getsize(OUT_PATH) / 1024
    print(f"\n✅ Сохранено: {OUT_PATH}")
    print(f"   Регионов: {len(new_features)}")
    print(f"   Размер: {size_kb:.1f} КБ")

if __name__ == "__main__":
    main()
