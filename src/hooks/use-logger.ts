import { useEffect } from "react";

const useLogger = (state: unknown) => {
    useEffect(() => {
        let message;
        if (typeof state === "object" && state !== null) message = "obj state: " + JSON.stringify(state, null, 4);
        else if (typeof state === "string") message = "str state: " + state;
        else message = "Prm state: " + state;
        console.log(message);
    }, [state]);
};

export { useLogger };
