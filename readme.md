# East Lake

>   A sumo project about eastlake map

```bash
pip3 install -r requirements.txt
```



## 1.Random trips

First , you should have a .net.xml file;

Then, if you don't want to design your own routers or trips by hand, you can choose to try the following command, which generates some random trips with the `RandomTrips.py` in `$SUMO_HOME/tools`

Notice! You should add the arg '--validate', which can avoid some unconnected roads. 

```commandline
python3 SUMO_HOME/tools/randomTrips.py -n map.net.xml  -e 3600 -p 3 --validate
```

After that , you can get two files: ` routes.rou.xml ` and `trips.trips.xml`. You can directly use `routes.rou.xml` in `.sumocfg`, such as followings:

```xml
    <input>
        <net-file value="map.net.xml" />
        <route-files value="routes.rou.xml" />
    </input>
```



