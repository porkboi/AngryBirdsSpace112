# AngryBirdsSpace112

Recreation of Angry Birds, ain't no way y'all don't know what that is. 
NO PLUGINS REQUIRED.

## How to play?

Run:

```
!pip install cmu-graphics
```
Navigate to the file directory using cd. Followed by:
```
py .\main.py
```

## Pipeline

- main.py is where levels are loaded and screened
- birds.py is where Bird Classes are defined and functions involving birds are defined, similarly for opp.py (pigs) and obstacles.py(blocks)
- levelLoader.py contained pre-coded levels
- timer.py ensures levels end
- parabolaPlot.py plots all trajectories of the bird before launch

## Gravity Simulation

### Earth Mode

Earth Gravity was simulated through calculus. Differentiating and Integrating a parabola. As such, this posed some limitations, such as the bord being unable to fly straight and the bird being unable to fly far. These were corrected in the updated algorithm for space.

### Space Mode

Space Gravity was simulated by separating the "bubble" around a planet into 4 quadrants, following different conventions and magnitudes to changesin x and y values accordingly. This allowed for oval-like trajectories around planets, and velocity to be higher nearer to the centre of the planet, while defining a constant acceleration magnitude for the birds perplanet.
