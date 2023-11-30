from CityGrid import CityGrid



cityGrid = CityGrid(14, 12, 0.6)
cityGrid.find_min_towers_map()
print(cityGrid.find_reliable_path(cityGrid.towers[1], cityGrid.towers[0]))
cityGrid.show_graphics_map()
cityGrid.find_best_coverage(500)
cityGrid.show_graphics_map()