defmodule Bridge.PyProxy do
    use GenServer

    require Logger

    def start_link(_args) do
        # TODO: implement the process pool for python node
        GenServer.start_link(__MODULE__, :ok, [name: :py_proxy])
    end

    def hello() do
        GenServer.call(py_process(), "hello")
    end

    def hello2(args) do
        GenServer.call(py_process(), {"hello2", args})
    end

    def self_crash() do
        GenServer.call(py_process(), "self_crash")
    end

    def do_crash() do
        GenServer.call(py_process(), "do_crash")
    end

    @impl true
    def init(_) do
        Process.flag(:trap_exit, true)
        {:ok, []}
    end

    @impl true
    def handle_info({_, :init_link, pid}, state) do
        Logger.log(:debug, "init link and monitor: #{inspect pid}")
        Process.link(pid)
        #Process.monitor(pid)
        {:noreply, state}
    end

    @impl true
    def handle_info({:DOWN, _ref, :process, pid, _}, state) do
        Logger.log(:debug, "DOWN event #{inspect pid}")
        {:noreply, state}
    end
  
    @impl true
    def handle_info({:EXIT, pid, reason}, state) do
        Logger.log(:debug, "exit event from: #{inspect pid}, reason: #{inspect reason}")
        {:noreply, state}
    end
  
    @impl true
    def handle_info(params, state) do
        Logger.log(:debug, "#{inspect params}")
        {:noreply, state}
    end

    defp py_process() do
        {:my_process, :"py@127.0.0.1"}
    end
end