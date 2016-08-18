# flask_mini_experiment
Flask mini-experiment. 

The goal of this project was to design and build a simple experiment to test whether there was some difference in likability between two sets of shirts (one set of 3 from designer A and one set of 3 from designed B). The experiment presents two shirts at a time and asks people to rate which would they'd prefer to buy. 

There's a requirements.txt in this folder so, if I understand correctly, you *should* be able to just "pip install -r requirements.txt" and get all the required packages. After getting things running, cd into the folder and run: python app.py to start the webserver and then navigate to: http://0.0.0.0:5000/ .

There are 2 designers and 3 shirts from each designer so there are 9 types of trials that we care about (all the pairwise comparisons). I've also counterbalanced which side the designers appeared on so including that there are 18 total types of trials (3 x 3 x 2). The experiment is built so that each block contains one version of these 18 trial types (randomized within a block). If this was a larger experiment, we might have more blocks (with breaks between them) but I only have one for now (so 18 total trials). Counterbalancing each block (and then randomizing within the trials within a block) allows us to look on a block by block level and still have things controlled. For instance, there might be learning or fatigue effects or whatever and then we could grab the first 2 blocks and the last 2 blocks and the conditions would all be controlled. This is a bit overboard for this toy experiment, but I wanted to build something that could scale (and something I could use for my experiments in the future!).

All of the shirts are _almost_ identical in aspect ratio, except one is slightly longer than the others. For this, I just rescaled that outlier to be the same as the others. This isn't something I would do for an actual experiment since warping the aspect ratio changes how the thing looks.

I set it up so that they have to click one of two radio buttons and then click a button in the center. This add a little time to the RTs, but I think it's better because it makes sure the mouse is in the same spot at the beginning of each trial and makes it equally close to both radio buttons. If they clicked the image rather than the button in the center, then when the next trial started their mouse would either already be on one of the images (biasing RT on that trial) or it we would magically move it to the center of the screen for them and that might be disorienting for them.

After the trials, the pandas dataframe I'm using to counterbalance and store all the information gets saved as '/Data/data.csv'. You can open it and see how I'm structuring things. For now, it gets overwritten each time you run the app.

