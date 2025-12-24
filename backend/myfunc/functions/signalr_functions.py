"""
SignalR related Azure Functions
"""
import azure.functions as func
import logging


def register_signalr_functions(app: func.FunctionApp):
    """
    Register all SignalR related functions to the main app
    
    Args:
        app: The main FunctionApp instance
    """
    
    @app.function_name(name="negotiate")
    @app.route(route="negotiate", auth_level=func.AuthLevel.ANONYMOUS)
    @app.generic_input_binding(arg_name="connectionInfo", type="signalRConnectionInfo", 
                               hubName="shanleeSignalR", 
                               connectionStringSetting="AZURE_SIGNALR_CONNECTION_STRING")
    def negotiate(req: func.HttpRequest, connectionInfo: str):
        """
        SignalR negotiate endpoint for establishing real-time connections
        """
        return func.HttpResponse(connectionInfo, mimetype="application/json")
    
    logging.info("SignalR functions registered")
