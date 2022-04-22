<div align="center">
<img src="https://user-images.githubusercontent.com/58790635/164586538-9c2fcfa8-0deb-4bd1-b3dd-20fd1f97ffc6.png" width="500"/>

# Inter-Dimensional Superhero League
A Python simulation of battles between random teams of superheros and villans from all your favorites multiverses.

<img src="https://user-images.githubusercontent.com/58790635/164584304-ce1a98bb-c07f-4a1d-b1ed-c498e5900008.png"  width="1250"/>
</div>

## Quickstart

Clone the repository
```
git clone https://github.com/cnsfeir/superhero-league.git
```

Create the virtual environment
```
cd superhero-league
python3 -m venv env
```

Activate the environment and install the dependencies
```
source env/bin/activate
pip install -r requirements.txt
```

Copy the `.fillme` file and fill it using your favorite text editor <br> 
List your Mailgun authorized recipients separated by commas (`,`) at the `VALID_MAILS` variable <br> 
Get an instantaneous execution with `SLOW_EXECUTION=0` and a slower step-by-step execution with `SLOW_EXECUTION=1`
```
cp .env.fillme .env
```

Enjoy your simulation! :tada: 
```
python3 main.py
```

