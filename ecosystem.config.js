module.exports = {
  apps : [{
    args: 'runserver 0:8000 --insecure',
    name: 'server',
    script: 'server.py',
    watch: false,
    instances: 4,
    exec_mode: 'cluster',
    max_memory_restart : "500M"
  }]
}