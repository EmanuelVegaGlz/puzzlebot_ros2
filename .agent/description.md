# Descripción de la actividad: Migración del stack de navegación a Puzzlebot

## Alcance de la actividad

En esta actividad se espera que tu equipo inicie la migración del stack de navegación desde TurtleBot3 hacia Puzzlebot.

Esto implica:

Dejar de depender exclusivamente de los paquetes de TurtleBot3.
Crear la estructura inicial de paquetes propia para tu robot.
Integrar el mundo de simulación construido en la actividad anterior.
Adaptar el flujo de simulación y mapeo al modelo de Puzzlebot.
Importante: en esta etapa se espera que la parte de SLAM ya quede funcional y afinada para tu robot y tu entorno. La parte de navegación debe quedar estructurada y ejecutable, pero todavía no se espera que esté completamente tuneada.

## Estructura esperada del proyecto

Se recomienda que el equipo estructure su proyecto en paquetes separados. Esta segmentación no es estrictamente obligatoria, pero es la forma más ordenada y recomendable de trabajar en ROS 2.

Una estructura sugerida es la siguiente:

puzzlebot_description: para URDF, Xacro, meshes y configuración del robot.
puzzlebot_gazebo: para el mundo, launch files de Gazebo, bridge, spawn del robot, ros2_control y configuraciones específicas de simulación.
puzzlebot_navigation2: para configuraciones de Nav2, AMCL, SLAM, costmaps, planners, mapas, YAMLs y perfiles de RViz.
Si tu equipo considera necesaria una separación adicional en más paquetes, puede hacerlo, siempre y cuando la estructura sea clara y consistente.

## Criterio de segmentación recomendado

El objetivo de separar el proyecto en varios paquetes es que cada parte tenga una responsabilidad clara.

Description: define cómo es el robot.
Simulation/Gazebo: define cómo se ejecuta el robot dentro del simulador.
Navigation: define cómo se comporta el stack de SLAM y navegación.
Esta separación es especialmente útil porque, más adelante, al migrar al robot físico, el paquete de simulación podrá retirarse o reemplazarse sin tener que reorganizar todo el proyecto.

Nota: hay elementos de simulación que inevitablemente viven en el URDF/Xacro, como ciertos tags de Gazebo o plugins de sensores. Eso es normal. Sin embargo, el lanzamiento de Gazebo, el bridge, el spawn del robot y la integración con ros2_control deben mantenerse separados de la lógica de navegación siempre que sea posible.

## Requisitos técnicos de la actividad

### 1. Paquete de descripción del robot

Deberán crear un paquete propio para el modelo del robot. En este paquete debe quedar organizada toda la información relacionada con:

URDF/Xacro del Puzzlebot
Dimensiones del robot
Frames principales
Sensores
Colisiones
Elementos del robot necesarios tanto para simulación como para navegación
Para este paquete se espera, como mínimo, la siguiente estructura de directorios:

- launch/
- meshes/
- rviz/
- urdf/

#### Carpeta launch/

Aquí deberán colocar el launch file principal para cargar la descripción del robot. Se recomienda que este archivo se llame:

puzzlebot_description.launch.xml
Si el equipo decide trabajar con launch files en Python, también es aceptable utilizar:

puzzlebot_description.launch.py
Importante: esta distinción depende del tipo de paquete y de la forma en que decidan construir su proyecto. Para este caso, se recomienda usar XML si el launch file es sencillo, ya que resulta más compacto y suficiente para cargar la descripción del robot.

#### Carpeta rviz/

Aquí deberán colocar la configuración de RViz asociada a la visualización del robot. Se recomienda que este archivo se llame:

puzzlebot_description.rviz
La idea es que este archivo permita abrir RViz y visualizar correctamente la descripción del Puzzlebot, sus frames y sus elementos principales.

#### Carpeta meshes/

Aquí deberán colocar los modelos 3D del robot. No se espera que todos usen exactamente la misma organización interna, pero sí se espera que los archivos estén segmentados de forma lógica.

Por ejemplo, pueden separar los meshes por categorías como:

- Base del robot
- Ruedas
- Sensores
- Componentes misceláneos

No se recomienda dejar todos los meshes mezclados en un solo directorio sin ningún criterio de organización.

#### Carpeta urdf/

Aquí deberán colocar los archivos URDF/Xacro del robot. Tampoco se espera que todos sigan exactamente la misma estructura interna, pero sí se espera que modularicen el robot.

Por ejemplo, pueden separar archivos por secciones como:

Base o estructura principal
Ruedas o partes mecánicas
Sensores
Control o componentes auxiliares
Un archivo principal que incluya al resto
No se recomienda que toda la definición del robot viva en un solo archivo enorme o que todos los Xacro/URDF queden al mismo nivel sin organización.

En resumen: no se les pide copiar exactamente una estructura de referencia, pero sí se espera que el paquete puzzlebot_description sea legible, modular y mantenible. La organización interna debe reflejar una separación clara entre visualización, descripción, modelos 3D y lanzamiento del robot.

### 2. Paquete de simulación

Deberán crear un paquete dedicado al entorno de simulación. En este paquete deben integrarse, como mínimo:

El archivo world o .sdf creado en la actividad anterior
Launch files para abrir Gazebo con su entorno
Launch files para hacer spawn del robot
Gazebo bridge para comunicar Gazebo con ROS 2
Integración con ros2_control o el mecanismo de control usado en simulación
Para este paquete se espera, como mínimo, la siguiente estructura de directorios:

config/
launch/
worlds/
Carpeta config/

Aquí deberán colocar archivos de configuración necesarios para la simulación. En particular, se espera que incluyan la configuración del bridge entre Gazebo y ROS 2. Se recomienda que este archivo se llame:

gazebo_bridge.yaml
En este archivo deberán declarar los topics que necesiten puentear entre Gazebo y ROS 2, por ejemplo sensores o información relevante para el stack de navegación.

#### Carpeta launch/

Aquí deberán colocar el launch file principal de simulación. Se recomienda que este archivo se llame:

puzzlebot_gazebo.launch.xml
Si el equipo prefiere usar launch files en Python, también es aceptable utilizar:

puzzlebot_gazebo.launch.py
Este launch file debe encargarse, directa o indirectamente, de:

Abrir Gazebo con el mundo correspondiente
Hacer spawn del robot en el entorno
Levantar el bridge
Integrar los elementos necesarios para que la simulación funcione con el stack

#### Carpeta worlds/

Aquí deberán colocar el archivo del entorno de simulación creado en la actividad anterior. Se recomienda utilizar un nombre claro y descriptivo, por ejemplo:

maze.world
Si el equipo utiliza un archivo en formato .sdf, también es válido, siempre y cuando quede claramente organizado dentro de esta carpeta.

El archivo contenido en worlds/ debe corresponder al entorno real del proyecto, no a un mundo genérico de ejemplo.

Importante: no se espera que todos los equipos tengan exactamente la misma implementación interna, pero sí se espera que separen claramente:

La configuración del bridge
Los launch files de simulación
Los archivos del mundo
No se recomienda dejar todo el contenido del paquete al mismo nivel o mezclar archivos de configuración, launch files y mundos sin ningún criterio.

En resumen: el paquete puzzlebot_gazebo debe contener de forma ordenada todo lo necesario para levantar el entorno simulado del proyecto. La organización interna debe dejar claro qué archivo configura el bridge, cuál lanza la simulación y cuál define el mundo del proyecto.

### 3. Paquete de navegación

Deberán comenzar la adaptación del stack de navegación a su robot y a su mapa. Este paquete debe contener, al menos, la configuración inicial necesaria para:

SLAM Toolbox
RViz (con sus respectivos perfiles para SLAM y navegación)
Nav2
Archivos YAML de configuración
Archivos del mapa generado o utilizados en navegación
Launch files relacionados con mapeo y navegación
Para este paquete se espera, como mínimo, la siguiente estructura de directorios:

config/
launch/
maps/
rviz/
scripts/ (si aplica)
Carpeta config/

Aquí deberán colocar los archivos de configuración principales del stack. Como mínimo, se espera que tengan archivos tipo YAML para:

Parámetros de Nav2, por ejemplo nav2_params.yaml
Parámetros de SLAM Toolbox, por ejemplo slam_toolbox.yaml
Si el equipo decide separar configuraciones adicionales por componente, también es válido, siempre y cuando mantengan una organización clara y consistente.

#### Carpeta launch/

Aquí deberán colocar los launch files principales del paquete de navegación. Se recomienda que al menos existan dos archivos claramente diferenciados:

slam.launch.xml o slam.launch.py
nav2.launch.xml o nav2.launch.py
La idea es que quede separado el flujo para:

Mapeo con SLAM
Navegación sobre un mapa ya existente
Si el equipo usa XML, se recomienda seguir esta opción por ser más compacta en launch files sencillos. Si prefieren Python, también es aceptable.

#### Carpeta maps/

Aquí deberán colocar los archivos de mapa generados o utilizados por el stack de navegación. Se espera que incluyan, como mínimo, el par correspondiente:

map_maze.pgm
map_maze.yaml
El nombre exacto puede variar, pero debe ser claro y descriptivo. La idea es que el mapa del proyecto quede identificado de manera inmediata y no se mezcle con mapas temporales o de prueba.

#### Carpeta rviz/

Aquí deberán colocar los perfiles de RViz asociados al paquete de navegación. Se recomienda que tengan, como mínimo, dos archivos:

slam.rviz
nav2.rviz
De esta forma podrán abrir directamente el perfil adecuado según el modo de trabajo:

Uno para mapeo
Otro para navegación autónoma.
Perfil slam.rviz

Este perfil debe estar orientado al proceso de mapeo. Como mínimo, se espera que incluya los siguientes marcadores de RViz:

Grid → nombre descriptivo sugerido: Grid
RobotModel → nombre descriptivo sugerido: RobotModel
TF → nombre descriptivo sugerido: TF
LaserScan → nombre descriptivo sugerido: LaserScan
Map → nombre descriptivo sugerido: Map
En este perfil se recomienda que el Fixed Frame sea map y que la visualización quede enfocada en ayudar a verificar:

La construcción del mapa
La orientación correcta del LiDAR
La relación entre frames
El comportamiento general del robot durante SLAM

Perfil nav2.rviz

Este perfil debe estar orientado a la navegación autónoma. Como mínimo, se espera que incluya los siguientes marcadores de RViz:

Grid → nombre descriptivo sugerido: Grid
RobotModel → nombre descriptivo sugerido: RobotModel
TF → nombre descriptivo sugerido: TF
LaserScan → nombre descriptivo sugerido: LaserScan
Map → nombre descriptivo sugerido: Map
Amcl Particle Swarm → nombre descriptivo sugerido: Amcl Particle Swarm
Adicionalmente, se espera que en este perfil organicen algunos marcadores dentro de carpetas para mantener una visualización más clara y profesional.

Carpeta Global Planner

Dentro de esta carpeta se espera que incluyan, como mínimo:

Map → nombre descriptivo sugerido: Global Costmap
Path → nombre descriptivo sugerido: Path
Polygon → nombre descriptivo sugerido: Polygon
Carpeta Controller

Dentro de esta carpeta se espera que incluyan, como mínimo:

Map → nombre descriptivo sugerido: Local Costmap
Path → nombre descriptivo sugerido: Local Plan
El objetivo de esta organización es que el perfil de navegación permita visualizar claramente:

El mapa general
Las partículas de AMCL
El costmap global
El costmap local
La trayectoria global
La trayectoria local que el robot intenta seguir

Importante: no es obligatorio que todos los equipos utilicen exactamente los mismos nombres descriptivos, pero sí se espera que los perfiles de RViz sean claros, ordenados y funcionales, y que mantengan separados los elementos de mapeo y los de navegación.

#### Carpeta scripts/

Esta carpeta es opcional, pero recomendable si el equipo desarrolla scripts auxiliares para pruebas o automatización. Por ejemplo:

Publicar la pose inicial
Enviar goals
Probar funcionalidades concretas del stack
Si no van a utilizar scripts, pueden omitir esta carpeta. Pero si la usan, deben mantenerla organizada y con nombres descriptivos.

Importante: no se espera que todos los equipos tengan exactamente la misma estructura interna ni exactamente los mismos nombres de archivo, pero sí se espera que la organización del paquete refleje una separación clara entre configuraciones, launch files, mapas, perfiles de RViz y scripts auxiliares.

No se recomienda mezclar todos estos elementos al mismo nivel dentro del paquete ni dejar configuraciones, mapas y launch files sin separación.

Recomendación sobre documentación: se recomienda que cada uno de sus paquetes incluya su propio archivo README.md explicando brevemente:

Qué contiene el paquete
Cuál es su propósito
Cómo se ejecuta o se utiliza
Esto les ayudará a mantener una mejor organización del proyecto y a facilitar el trabajo en equipo.

Recomendación sobre estructura global del workspace: dentro de su entorno de ROS 2 se recomienda crear un workspace exclusivo para este proyecto llamado:

puzzlebot_ws
Dentro de la carpeta src/ de ese workspace, se recomienda crear una carpeta adicional llamada:

puzzlebot_ros2
Dentro de esa carpeta podrán colocar:

Un README.md global del proyecto
El paquete puzzlebot_description
El paquete puzzlebot_gazebo
El paquete puzzlebot_navigation2
Por ejemplo, una estructura global recomendable sería:

puzzlebot_ws/
└── src/
    └── puzzlebot_ros2/
        ├── puzzlebot_description/
        ├── puzzlebot_gazebo/
        ├── puzzlebot_navigation2/
        └── README.md
Esta organización ayuda a mantener una estructura lógica, mantenible y funcional tanto en ROS 2 como en GitHub. Además, facilita que el repositorio tenga una organización profesional y que cualquier integrante del equipo pueda entender rápidamente la arquitectura general del proyecto.

## Integración del mapa y del mundo

Además de integrar el robot, en esta actividad deberán integrar formalmente el mapa definido en la actividad anterior.

Esto incluye:

Incorporar el archivo world o .sdf del entorno
Asegurarse de que el robot puede aparecer correctamente dentro de ese mundo
Verificar que a pesar de tener el mapa ya generado, todavía puedan ejecutar el modo SLAM
Utilizar el mapa generado o base del proyecto como referencia para el modo de navegación
El objetivo ya no es trabajar sobre un entorno genérico de TurtleBot3, sino sobre el mapa y el mundo que ustedes mismos construyeron para el proyecto final.

## Qué debe estar listo al finalizar esta actividad

El paquete de descripción del robot creado y compilado correctamente.
El paquete de simulación creado e integrado correctamente en el mundo del proyecto.
El paquete de navegación creado y compilado correctamente.
La configuración de SLAM adaptada y funcionando con Puzzlebot.
La base del modo de navegación creada, considerando el mapa desarrollado en la actividad anterior.
Un perfil de RViz para SLAM y otro para navegación, con los marcadores y visualizaciones correctos.
Un repositorio público de GitHub con el proyecto del equipo.

## Checklist obligatorio de integración

1. TF correcto.

El árbol de frames debe estar correctamente planteado. Como mínimo, deberán revisar y validar:

base_link
base_footprint
odom
map
2. Sensores.

El LiDAR debe estar correctamente integrado en el robot y en la simulación. Deben revisar:

topic correcto del scan
frame_id correcto
Orientación correcta del sensor
Coherencia entre URDF/Xacro, Gazebo y Nav2
3. URDF/Xacro.

El modelo del robot debe representar correctamente el hardware. Deben revisar:

Dimensiones correctas
Frames bien nombrados
Colisiones razonables
Elementos de simulación integrados de forma consistente
4. Control.

La simulación debe responder de forma coherente con la física del robot. Deben revisar:

Velocidades lineales y angulares coherentes
Parámetros físicos del robot
Integración de ros2_control o del mecanismo de control que estén utilizando en simulación
5. Mundo y mapa.

El entorno del proyecto debe estar correctamente integrado. Deben revisar:

Que el archivo world cargue correctamente
Que el robot aparezca en la posición correcta dentro del entorno
Que el mundo utilizado corresponda con el mapa del proyecto
Que el stack de SLAM y navegación se esté probando sobre su propio entorno y no sobre un ejemplo genérico

## Evidencia (Demo)

En el video deberá mostrarse, como mínimo, lo siguiente:

El lanzamiento en modo SLAM
Que el entorno y el robot cargan correctamente en simulación
Que RViz muestra los marcadores apropiados para mapeo
Que el robot avanza al menos un poco dentro del entorno
Que el mapa se va generando
Además, en el mismo video deberán mostrar:

El lanzamiento en modo navegación
Que el robot aparece correctamente spawneado en el entorno
Que el mapa cargado corresponde al mapa correcto del proyecto
Que RViz muestra los marcadores apropiados para navegación.
Importante: no se espera que la navegación ya esté completamente afinada. Lo que se evaluará aquí es que la estructura del proyecto ya contemple ambos modos y que puedan ejecutarse correctamente desde su bringup.
