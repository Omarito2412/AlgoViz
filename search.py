from Tkinter import *
class Game:
    def __init__(self,width, height, color='#000000', bone_pos=(520, 250), doge_pos=(90, 200)):
        root = Tk()     # Initialize the GUI window
        root.geometry(str(width)+"x"+str(height))    # Set the window size
        root.minsize(width=300, height=300) # Minimum window size
        root.maxsize(width= 700, height=500)# Maximum window size
        root.wm_title("Hungry Doge's Quest")           # Window name
        self.canvas = Canvas(root, width=width, height=height)  # Create the canvas
        corners = [0, 0, 0, height-1, width-1, 0, width-1, height-1]    # Polygon's corners
        # Create the polygon to fill the canvas
        self.canvas.create_polygon(corners, outline=color, fill=color, smooth=False, width=width)
        self.canvas.pack(fill=BOTH, expand=YES) # Pack the polygon into the canvas

        bone = PhotoImage(file='bone.gif')  # Create PhotoImage from gif file
        self.canvas.create_image(bone_pos[0], bone_pos[1], image=bone) # The goal node


        self.goal = bone_pos
        self.init = doge_pos
        self.iterations = 0      # Emergency break from the algorithm
        solution = self.Search(algorithm="bfs", precision=5)

        self.paintPath(solution)

        doge = PhotoImage(file = 'doge.gif')    # Create PhotoImage from gif file
        self.canvas.create_image(doge_pos[0], doge_pos[1], image=doge)    # Add the image to canvas

        root.mainloop()
    """ 
        Returns a list of tuples.
        Each tuple is a child (Possible move) from
        the given node.
    """
    def nodeChildren(self, pos, precision=1):
        children = []
        range0 = [pos[0] - precision, pos[0], pos[0] + precision]
        range1 = [pos[1] - precision, pos[1], pos[1] + precision]
        for x in range0:
            for y in range1:
                if((x, y) == pos):
                    continue
                children.append((x, y))
        return children
    """
        Perform Breadth first search 
        from the given init to reach
        the goal if possible
    """
    def Search(self, mark=True, algorithm="bfs", precision=1):
        fringe = []         # The fringe that will hold the moves
        paths = dict()           # The path to the goal
        visited = dict()    # The dicitionary that will label visited nodes
        fringe.append(self.init)    # Add the initial node to the fringe
        paths[self.init] = ()       # Path to initial node
        while(len(fringe) > 0):     # Keep repeating so long we haven't explored everything
            # if(self.iterations > 50000):    # For now it takes a lot of time, need to break
            #     return ()
            self.iterations += 1
            if(algorithm == "bfs"):
                currentNode = fringe.pop(0)  # Pop a node following FIFO (Queue behavior)
            else:
                currentNode = fringe.pop()  # Pop a node following LIFO (Stack behavior)
            if(
                abs(currentNode[0] - self.goal[0]) <= precision
                and abs(currentNode[1] - self.goal[1]) <= precision
            ):   # Are we there yet?
                return paths[currentNode]   # Wohoo!
            
            # Loop through all currentNode's children
            for node in self.nodeChildren(currentNode, precision=precision): 
                if(
                    (int(node[0]) >= 0)    # Doesn't exceed boundaries
                    and (int(node[1]) >= 0) # Doesn't exceed boundaries
                    and (int(node[0]) <= int(self.canvas["width"])) # Doesn't exceed boundaries
                    and (int(node[1]) <= int(self.canvas["height"]))# Doesn't exceed boundaries
                    and node not in visited     # Wasn't visited before
                    ):
                    fringe.append(node)     # Undiscovered node, Add to the fringe
                    paths[node] = []        # Path is through parent (currentNode)
                    paths[node].extend(paths[currentNode])
                    paths[node].append(node)
                    visited[node] = 1       # Mark as visited

                    # Illustrate the search strategy
                    if(mark):
                        self.canvas.create_oval(node[0], node[1], node[0], node[1], outline="yellow")
        return ()
    """
        Now that we've found the solution
        lets paint the path for doge to 
        reach the bone.
    """
    def paintPath(self, solution):
        for node in solution:
            self.canvas.create_oval(node[0], node[1], node[0]+4, node[1]+4, outline="green", fill="green")

game = Game(600, 400, '#4C88A0', bone_pos=(340, 200), doge_pos=(540, 330))