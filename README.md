# Card game model

## Requirements

Card game model requires **python 3.9** and all dependencies at `requirements.txt` installed.

## Execution

To run model you should:
- go to the root folder of model;

- enter the command like:
    ```
    python -m card_game -t 1000 -r
    ```

    The command supports arguments:
    - `-t <int>` - number of timesteps to run. Default is 3000;
    - `-r` - create report. Report as html page will be saved in `/reports` folder;

Alternatively, you can run notebooks in `/notebooks` folder.

## Testing

Card game model uses `pytest` for unit and integration testing. In order to make use of it, just pass in root directory:

```
python -m pytest
```
