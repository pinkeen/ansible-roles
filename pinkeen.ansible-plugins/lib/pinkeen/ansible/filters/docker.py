from pinkeen.ansible.filters import filterclass


@filterclass
class DockerFilters(object):
  
  @staticmethod
  def do_docker_ports_proto_split(cfg={}, default_proto='tcp'):
      protos = {}

      for k, v in cfg.items():
        port, *proto = k.split('/')

        port = int(port.strip())
        proto = proto[0] if len(proto) and proto[0].strip() != '' else default_proto
        proto = proto.strip()

        if not proto in protos:
          protos[proto] = {}

        protos[proto][port] = v;

      return protos


  @staticmethod
  def do_docker_env_to_dict(env=[]):
      return { 
        name.strip(): value[0].strip() if len(value) else None
          for name, *value in 
            map(lambda item: item.split('=', 1), env)
      }

