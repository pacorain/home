# Home Assistant Packages

I've organized my Home Assistant config into [packages]
(https://www.home-assistant.io/docs/configuration/packages/) that each group
certain functionality of the smart home together.

Each package has its own folder, with a `package.yaml` file containing the 
package's configuration. Each package.yaml file is then added to 
[index.yaml](index.yaml) to bring it into my Home Assistant config. This allows
me to quickly disable and enable pieces of my smart home.