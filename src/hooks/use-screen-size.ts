import { useEffect, useMemo, useState } from "react";

// height
const HEIGHT_SM = 480;
const HEIGHT_MD = 768;
const HEIGHT_LG = 1024;
// const HEIGHT_XL = 1200;

// width
const WIDTH_SM = 640;
const WIDTH_MD = 768;
const WIDTH_LG = 1024;
// const WIDTH_XL = 1280;

const useDefaultScreenSizes = () => {
    // height
    const [isSmallHeight, setIsSmallHeight] = useState<boolean>(false); // 0 - 480px
    const [isMediumHeight, setIsMediumHeight] = useState<boolean>(false); // 481 - 768px
    const [isLargeHeight, setIsLargeHeight] = useState<boolean>(false); // 769 - 1024px
    const [isExtraHeight, setIsExtraHeight] = useState<boolean>(false); // 1025px+
    const heightSetters = useMemo(() => {
        return [setIsSmallHeight, setIsMediumHeight, setIsLargeHeight, setIsExtraHeight];
    }, [setIsSmallHeight, setIsMediumHeight, setIsLargeHeight, setIsExtraHeight]);
    // width
    const [isSmallWidth, setIsSmallWidth] = useState<boolean>(false); // 0 - 640px
    const [isMediumWidth, setIsMediumWidth] = useState<boolean>(false); // 641 - 768px
    const [isLargeWidth, setIsLargeWidth] = useState<boolean>(false); // 769 - 1024px
    const [isExtraWidth, setIsExtraWidth] = useState<boolean>(false); // 1025px+
    const widthSetters = useMemo(() => {
        return [setIsSmallWidth, setIsMediumWidth, setIsLargeWidth, setIsExtraWidth];
    }, [setIsSmallWidth, setIsMediumWidth, setIsLargeWidth, setIsExtraWidth]);

    useEffect(() => {
        // queries
        // height
        const heightQueries = [
            window.matchMedia(`(max-height: ${HEIGHT_SM}px)`), // small
            window.matchMedia(`(min-height: ${HEIGHT_SM + 1}px) and (max-height: ${HEIGHT_MD}px)`), // medium
            window.matchMedia(`(min-height: ${HEIGHT_MD + 1}px) and (max-height: ${HEIGHT_LG}px)`), // large
            window.matchMedia(`(min-height: ${HEIGHT_LG + 1}px)`), // extra
        ];
        // width
        const widthQueries = [
            window.matchMedia(`(max-width: ${WIDTH_SM}px)`), // small
            window.matchMedia(`(min-width: ${WIDTH_SM + 1}px) and (max-width: ${WIDTH_MD}px)`), // medium
            window.matchMedia(`(min-width: ${WIDTH_MD + 1}px) and (max-width: ${WIDTH_LG}px)`), // large
            window.matchMedia(`(min-width: ${WIDTH_LG + 1}px)`), // extra
        ];

        // defaults
        // height
        heightSetters.forEach((setter: (state: boolean) => void, i: number) => {
            setter(heightQueries[i].matches);
        });
        // width
        widthSetters.forEach((setter: (state: boolean) => void, i: number) => {
            setter(widthQueries[i].matches);
        });

        // handlers
        // height
        const heightHandlers = [
            () => setIsSmallHeight(heightQueries[0].matches), // small
            () => setIsMediumHeight(heightQueries[1].matches), // medium
            () => setIsLargeHeight(heightQueries[2].matches), // large
            () => setIsExtraHeight(heightQueries[3].matches), // extra
        ];
        // width
        const widthHandlers = [
            () => setIsSmallWidth(widthQueries[0].matches), // small
            () => setIsMediumWidth(widthQueries[1].matches), // medium
            () => setIsLargeWidth(widthQueries[2].matches), // large
            () => setIsExtraWidth(widthQueries[3].matches), // extra
        ];

        // add event listeners
        // height
        heightQueries.forEach((query: MediaQueryList, i: number) => {
            query.addEventListener("change", heightHandlers[i]);
        });
        // width
        widthQueries.forEach((query: MediaQueryList, i: number) => {
            query.addEventListener("change", widthHandlers[i]);
        });

        // cleanups
        return () => {
            // remove event listeners
            // height
            heightQueries.forEach((query: MediaQueryList, i: number) => {
                query.removeEventListener("change", heightHandlers[i]);
            });
            // width
            widthQueries.forEach((query: MediaQueryList, i: number) => {
                query.removeEventListener("change", widthHandlers[i]);
            });
        };
    }, [heightSetters, widthSetters]);

    return {
        // height
        isSmallHeight, // 0 - 480px
        isMediumHeight, // 481 - 768px
        isLargeHeight, // 769 - 1024px
        isExtraHeight, // 1200px+
        // width
        isSmallWidth, // 0 - 640px
        isMediumWidth, // 641 - 768px
        isLargeWidth, // 769 - 1024px
        isExtraWidth, // 1280px+
    };
};

const useMatchSize = (matchMedia: string) => {
    const [isConstrainedSize, setIsConstrainedSize] = useState<boolean>(false);

    if (
        !(
            (matchMedia.includes("-height") || matchMedia.includes("-width")) &&
            (matchMedia.includes("max") || matchMedia.includes("min"))
        )
    ) {
        throw new Error("Invalid media query format. Use 'max-height', 'min-height', 'max-width', or 'min-width'.");
    }

    useEffect(() => {
        const mediaQuery = window.matchMedia(matchMedia);
        setIsConstrainedSize(mediaQuery.matches);

        const handleSizeChange = () => {
            return setIsConstrainedSize(mediaQuery.matches);
        };
        mediaQuery.addEventListener("change", handleSizeChange);

        return () => mediaQuery.removeEventListener("change", handleSizeChange);
    }, [matchMedia]);

    return isConstrainedSize;
};

export { useDefaultScreenSizes, useMatchSize };
