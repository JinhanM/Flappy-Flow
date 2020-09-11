### Flappy-Flow, An AI based on NEAT master flappy bird



#### Introduction to functions

​	There are three items in the repository, "flappy bird.py" and "flappy bird NEAT.py". 



​	"flappy bird.py" is a self-build classic flappy bird game, you can press space to make the bird "fly" once. The bird will die if the bird crush into the pipe or the ground.



​	"flappy bird NEAT.py" is the core of the project. There are two part in the main function, "run(config_path)", and "replay_genome(config_path, model_path)". The first function, "run()" is the training function, it will send 50 flappy birds with random control logic into the game at once, select and evolve the bird with the best performance. The training will be stop if the bird reaches 20 points, which we would like to say a bird with 20 points is a bird mastering this game, or in other words, we say a bird can reach 20 points can also keep playing and get 1,000 points. Since this game is a relative easy game, the training will always finishes within 2 generation, 10 seconds.



​	"replay_genome()" is a function for demo the best fitted model to play the flappy bird, you would see that it can play on and on forever. Approximately it will reach 1,500 points in an hour.



#### NEAT

​	The AI is based on NEAT, Neuroevolution of augmenting topologies. The basic idea is to generate a bunch of random population, and let them perform the task. By choosing a small set of the best performed models and let them "breed" the next generation with "mutation" allowed, the model will take the revolution and get better performance until it can master the task. It took the idea of evolution and place it into the AI.

​	

​	The paper of NEAT is at the link below. I highly recommand to read through the paper:

​	http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf





#### Reference:

​	TechwithTim

​	Clear Code Python