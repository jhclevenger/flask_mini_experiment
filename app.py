#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import time

app = Flask(__name__)

trials_per_block = 18 # 3 (designer 1 shirts) x 3 (designer 2 shirts) x 2 (which designer on which side)
blocks = 1 # ideally we'd want multiple blocks to average out random error

def counterbalance(trials_per_block, blocks):
    
    # create dataframe to store trial info
    total_trials = blocks * trials_per_block
    data = pd.DataFrame({'trial': [], 'shirt_d01': [], 'shirt_d02': [], 'side_d01': [], 'response_d01': [],
                         'response_d02': [], 'rt': []})
    block = pd.DataFrame.copy(data)
    # participant = participant number
    # trial = trial number
    # shirt_designer_01: which shirt from designer 1 was displayed (0:2)
    # shirt_designer_02: which shirt from designer 2 was displayed (0:2)
    # side_designer_01: which side designer 1 shirt was on
    # response_designer_01: 1 = designer 1 was chosen on this trial, 0 = not chosen
    # response_designer_02: 1 = designer 2 was chosen on this trial, 0 = not chosen
    # rt: response time

    # counterbalance shirt presentations
    shirt_01 = np.array([0, 1, 2])
    block.shirt_d01 = np.tile(shirt_01, trials_per_block / len(shirt_01))
    shirt_02 = np.array([0, 1, 2])
    shirt_02 = np.repeat(shirt_02,3)
    block.shirt_d02 = np.tile(shirt_02, trials_per_block / len(shirt_02))

    # counterbalance which designer appears on which side
    d1_side = np.array(['left', 'right'])
    block.side_d01 = np.repeat(d1_side, trials_per_block / len(d1_side))

    # create all blocks preserving the counterbalancing within each block.
    # this allows us to cleanly look at learning/fatigue/whatever effects on a block by block level
    for i_block in range(blocks):
        shuffled_block = block.iloc[np.random.permutation(len(block))]
        shuffled_block.reset_index(drop=True)
        frames = (shuffled_block, data)
        data = pd.concat(frames)

    data = data.reset_index(drop = True)
    data.trial = range(total_trials)
    
    return data

data = counterbalance(trials_per_block, blocks)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        return redirect(url_for('trial', id=0))
    return render_template('index.html')

@app.route('/trial/<int:id>', methods=['GET', 'POST'])
def trial(id):
    
    global data
    d01_shirts = ["/static/images/d01_01.jpg","/static/images/d01_02.jpg","/static/images/d01_03.jpg"]
    d02_shirts = ["/static/images/d02_01.jpg","/static/images/d02_02.jpg","/static/images/d02_03.jpg"]
    
    # end of experiment or if someone manually enters a larger url
    if id >= len(data): 
        return redirect(url_for('finish'))
    
    if request.method == 'GET':
        
        # decide which shirts to display
        if data.side_d01[id] == 'left':
            left_image = d01_shirts[int(data.shirt_d01[id])]
            right_image = d02_shirts[int(data.shirt_d02[id])]
        else:
            left_image = d02_shirts[int(data.shirt_d02[id])]
            right_image = d01_shirts[int(data.shirt_d01[id])]
        
        # save response start    
        data.rt.loc[id] = time.time() 
        return render_template('trial.html', left_image=left_image, right_image=right_image)
    
    # get response
    answer = request.form.get('answer')
    if answer and answer in ('right','left'):
        
        # calculate rt
        data.rt.loc[id] = time.time() - data.rt.loc[id]
        
        # record response
        if answer == data.side_d01[id]:
            data.response_d01.loc[id] = 1
            data.response_d02.loc[id] = 0
        else:
            data.response_d01.loc[id] = 0
            data.response_d02.loc[id] = 1
        id+=1
        
    return redirect(url_for('trial', id=id))

@app.route('/finish')
def finish():
    data.to_csv('data/data.csv',index=False)
    return render_template("finish.html",
                           designer_01_mean=np.round(np.mean(data.response_d01),3)*100,
                           designer_01_rt=np.round(np.mean(data.rt[data.response_d01 == 1]),2),
                           designer_02_mean=np.round(np.mean(data.response_d02),3)*100,
                           designer_02_rt=np.round(np.mean(data.rt[data.response_d02 == 1]),2))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)