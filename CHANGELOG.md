## 0.4.0 (2025-05-02)

### Feat

- **test_world_gen.py**: created proper testing gui
- **world.py**: added movement costs and visibility multipliers
- **test_world.py**: added ability to see properties of hovered ground, realtime variable changing, etc
- **world.py**: replaced the fully random world gen with a more natural looking one + proper typing

### Fix

- **simulation.py**: updated to work with newest world.py
- fixed some import compatibility issues
- **world.py**: fixed an infinite loop stemming from the generate_map function

### Refactor

- **test_world_gen.py**: changed while loop, renamed main to run

## 0.2.0 (2025-04-25)

### Feat

- **animals.py**: implementing basic animal base class
- **animals.py**: basic implementation of the animal base class
- **world.py**: implementing map class with basic methods

### Fix

- **animals.py**: fixed typing and stopped animals going off screen
