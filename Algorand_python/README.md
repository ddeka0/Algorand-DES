#### Instruction to run the project:

        sudo -H pip3 install sortedcontainers
        sudo -H pip3 install numpy
        sudo -H pip3 install ecdsa
        python3 main.py
        
#### Usage:

        usage: main.py [-h] [-n MAX_NODES] [-fan FAN_OUT] [-md NON_BLOCK_DELAY_MEAN]
                       [-vd NON_BLOCK_DELAY_SIGMA] [-mD BLOCK_DELAY_MEAN]
                       [-vD BLOCK_DELAY_SIGMA] [-tstep TOU_STEP] [-tprop TOU_PROP]
                       [-tfinal TOU_FINAL] [-st MAX_ALGORAND] [--version]

        optional arguments:
          -h, --help            show this help message and exit
          -n MAX_NODES          set MAX_NODES
          -fan FAN_OUT          set GOSSIP_FAN_OUT
          -md NON_BLOCK_DELAY_MEAN
                                set NON_BLOCK_MSG_DELAY_MEAN
          -vd NON_BLOCK_DELAY_SIGMA
                                set NON_BLOCK_MSG_DELAY_SIGMA
          -mD BLOCK_DELAY_MEAN  set BLOCK_MSG_DELAY_MEAN
          -vD BLOCK_DELAY_SIGMA
                                set BLOCK_MSG_DELAY_SIGMA
          -tstep TOU_STEP       set tou_step
          -tprop TOU_PROP       set tou_prop
          -tfinal TOU_FINAL     set tou_final
          -st MAX_ALGORAND      set MAX_ALGORAND
          --version             show program's version number and exit
          
          You can delete generated key and delays file using the command git clean -f

![Simulation](https://github.com/ddeka0/CS620-Algorand-DES/blob/master/algorand.gif)
