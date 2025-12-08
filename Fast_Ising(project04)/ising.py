import numpy as np
from PIL import Image, ImageDraw
from scipy import signal
from decorator01 import TimerDecorator


class ising_simulation:
    """
    Class for simulating 2D Ising model using Metropolis algorithm.

    Attributes:
        arr_size (int): Size of the square lattice (arr_size x arr_size).
        j (float): Interaction strength between neighboring spins.
        beta (float): Inverse temperature (1/kT).
        force_B (float): External magnetic field strength.
        bigsteps (int): Number of big steps (each consisting of multiple small steps).
        ups_density (float): Initial density of up spins (+1).
        img_filename (str): Filename to save the final spin configuration image.
        animation_filename (str): Filename to save the animation of the simulation.
        magnetisation_filename (str): Filename to save the magnetization data.

    Methods:
        show_array(): Displays the current spin configuration as an image.
        calculate_hamiltionian(): Calculates and prints the Hamiltonian of the current configuration.
        small_step(): Performs a single Metropolis update on a randomly chosen spin.
        big_step(): Performs a full sweep of Metropolis updates over the entire lattice.
        simulate(): Runs the simulation for the specified number of big steps.
        calculate_M(): Calculates and returns the magnetization of the current configuration.
    """
    def __init__(self, 
                 arr_size, 
                 j, 
                 beta, 
                 force_B, 
                 amount_of_steps, 
                 ups_density = 0.5, 
                 img_filename = None,
                 animation_filename = None,
                 magnetisation_filename = None):
        self.j = j
        self.beta = beta
        self.force_B = force_B
        self.bigsteps = amount_of_steps
        self.ups_density = ups_density
        self.img_filename = img_filename
        self.animation_filename = animation_filename
        if animation_filename != None:
            self.animation_frames = []
        self.magnetisation_filename = magnetisation_filename
        self.hamiltionian = 0
        self.neighborhood_kernel = np.array([[0, 1, 0],
                                                [1, 0, 1],
                                                [0, 1, 0]])

        self.M = (-1)*np.ones([arr_size, arr_size], dtype=np.int8)
        amount_of_ups = int(self.ups_density * self.M.size)
        idxes = np.random.choice(self.M.size, amount_of_ups, replace=False)
        self.M.flat[idxes] = 1


    def draw_array(self, number, show=False):
        image_size = 1000
        image = Image.new('RGB', (image_size, image_size), 'black')
        draw = ImageDraw.Draw(image)

        red_color = '#f0827a'
        blue_color = '#7ab3f0'

        matrix_width = self.M.shape[0]
        dw = np.floor(image_size/matrix_width)
        color = 'white'
        for x in range(matrix_width):
            for y in range(matrix_width):
                if self.M[x,y] == 1:
                    color = red_color
                else:
                    color = blue_color

                draw.rectangle([x*dw, y*dw, (x+1)*dw, (y+1)*dw], fill=color)

        if show == True:
            image.show()

        if self.img_filename != None:
            image.save(f'{self.img_filename}{number:04d}.png')

        if self.animation_filename != None:
            self.animation_frames.append(image)


    def calculate_hamiltionian(self):
        self.hamiltionian = (-1) * 1/2 * self.j * (  \
                self.M * signal.convolve2d(self.M, self.neighborhood_kernel, mode = 'same') \
                    ).sum() \
            - self.force_B * self.M.sum()
        print(self.hamiltionian)
  

    def small_step(self):
        idx_x, idx_y = np.random.randint(0, self.M.shape[0], size=2)
        s_i = self.M[idx_x, idx_y]
        kh, kw = self.neighborhood_kernel.shape
        assert kh % 2 == 1 and kw % 2 == 1, "Kernel must have odd shape."
        ph, pw = kh // 2, kw // 2

        # pad and extract the patch centered at (idx_x, j)
        Mp = np.pad(self.M, ((ph, ph), (pw, pw)), mode='constant')
        patch = Mp[idx_x:idx_x+kh, idx_y:idx_y+kw]  # because Mp is shifted by padding
        
        E_0 = (-1) * 1/2 * self.j * (  \
                s_i * signal.convolve2d(patch, self.neighborhood_kernel, mode = 'same') \
                    ).sum() \
            - self.force_B * patch.sum()

        E_1 = (-1) * 1/2 * self.j * (  \
                (-1) * s_i * signal.convolve2d(patch, self.neighborhood_kernel, mode = 'same') \
                    ).sum() \
            - self.force_B * patch.sum()
        
        delta_E = E_1 - E_0
        if delta_E < 0:
            self.M[idx_x, idx_y] *= (-1)
        else:
            prob = np.exp( (-1) * self.beta * delta_E )
            if np.random.rand() < prob:
                self.M[idx_x, idx_y] *= (-1)


    def big_step(self):
        for _ in range(self.M.size):
            self.small_step()


    # Visualisation and output methods
    def calculate_M(self):
        return 1/self.M.size * self.M.sum()
    

    def save_M(self, step, create_file=False):
        if self.magnetisation_filename != None:
            if create_file == True:
                with open(self.magnetisation_filename, 'w') as f:
                    f.write('Step\tMagnetisation\n')

            with open(self.magnetisation_filename, 'a') as f:
                f.write(f'{step}\t{self.calculate_M()}\n')


    # Main simulation method
    def simulate_save(self):
        i = 0
        self.draw_array(i)
        self.save_M(i, True)
        i += 1
        for _ in range(self.bigsteps):
            self.big_step()
            self.draw_array(i)
            self.save_M(i)
            i += 1

        if self.animation_filename != None:
            self.animation_frames[0].save(self.animation_filename,
                                          save_all=True,
                                          append_images=self.animation_frames[1:],
                                          duration=200)
    

    @TimerDecorator
    def simulate(self):
        i = 0
        i += 1
        for _ in range(self.bigsteps):
            self.big_step()
            i += 1

