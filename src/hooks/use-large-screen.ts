import { useEffect, useState } from "react";

const LARGE_SCREEN = "1024"; //px

const useIsLargeScreen = () => {
    const [isLargeScreen, setIsLargeScreen] = useState<boolean>(false);

    useEffect(() => {
        const mediaQuery = window.matchMedia(`(min-width: ${LARGE_SCREEN}px)`);
        setIsLargeScreen(mediaQuery.matches);

        const handleMediaChange = (e: MediaQueryListEvent) => {
            setIsLargeScreen(e.matches);
        };

        mediaQuery.addEventListener("change", handleMediaChange);

        return () => mediaQuery.removeEventListener("change", handleMediaChange);
    }, []);

    return isLargeScreen;
};

export { useIsLargeScreen };
