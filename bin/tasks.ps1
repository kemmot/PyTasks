$Path = Split-Path $script:MyInvocation.MyCommand.Path
$ModulePath = Resolve-Path "$Path\..\tasks"
python $ModulePath $args