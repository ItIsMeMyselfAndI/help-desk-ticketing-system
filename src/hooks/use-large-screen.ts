import { useEffect, useState } from "react";

const useScreenSize = () => {
    // height
    const [isSmallHeight, setIsSmallHeight] = useState<boolean>(false); // 0 - 640px
    const [isMediumHeight, setIsMediumHeight] = useState<boolean>(false); // 641 - 768px
    const [isLargeHeight, setIsLargeHeight] = useState<boolean>(false); // 769 - 1024px
    const [isExtraHeight, setIsExtraHeight] = useState<boolean>(false); // 1025px+

    // width
    const [isSmallWidth, setIsSmallWidth] = useState<boolean>(false); // 0 - 640px
    const [isMediumWidth, setIsMediumWidth] = useState<boolean>(false); // 641 - 768px
    const [isLargeWidth, setIsLargeWidth] = useState<boolean>(false); // 769 - 1024px
    const [isExtraWidth, setIsExtraWidth] = useState<boolean>(false); // 1025px+

    useEffect(() => {
        // height
        const smallHeightQuery = window.matchMedia(`(max-height: 640px)`);
        const mediumHeightQuery = window.matchMedia(`(min-height: 641px) and (max-height: 768px)`);
        const largeHeightQuery = window.matchMedia(`(min-height: 769px) and (max-height: 1024px)`);
        const extraHeightQuery = window.matchMedia(`(min-height: 1025px)`);

        // width
        const smallWidthQuery = window.matchMedia(`(max-width: 640px)`);
        const mediumWidthQuery = window.matchMedia(`(min-width: 641px) and (max-width: 768px)`);
        const largeWidthQuery = window.matchMedia(`(min-width: 769px) and (max-width: 1024px)`);
        const extraWidthQuery = window.matchMedia(`(min-width: 1025px)`);

        // height
        setIsSmallHeight(smallHeightQuery.matches);
        setIsMediumHeight(mediumHeightQuery.matches);
        setIsLargeHeight(largeHeightQuery.matches);
        setIsExtraHeight(extraHeightQuery.matches);

        // width
        setIsSmallWidth(smallWidthQuery.matches);
        setIsMediumWidth(mediumWidthQuery.matches);
        setIsLargeWidth(largeWidthQuery.matches);
        setIsExtraWidth(extraWidthQuery.matches);

        // height
        const handleSmallHeight = () => setIsSmallHeight(smallHeightQuery.matches);
        const handleMediumHeight = () => setIsMediumHeight(mediumHeightQuery.matches);
        const handleLargeHeight = () => setIsLargeHeight(largeHeightQuery.matches);
        const handleExtraHeight = () => setIsExtraHeight(extraHeightQuery.matches);

        // width
        const handleSmallWidth = () => setIsSmallWidth(smallWidthQuery.matches);
        const handleMediumWidth = () => setIsMediumWidth(mediumWidthQuery.matches);
        const handleLargeWidth = () => setIsLargeWidth(largeWidthQuery.matches);
        const handleExtraWidth = () => setIsExtraWidth(extraWidthQuery.matches);

        // height
        smallHeightQuery.addEventListener("change", handleSmallHeight);
        mediumHeightQuery.addEventListener("change", handleMediumHeight);
        largeHeightQuery.addEventListener("change", handleLargeHeight);
        extraHeightQuery.addEventListener("change", handleExtraHeight);

        // width
        smallWidthQuery.addEventListener("change", handleSmallWidth);
        mediumWidthQuery.addEventListener("change", handleMediumWidth);
        largeWidthQuery.addEventListener("change", handleLargeWidth);
        extraWidthQuery.addEventListener("change", handleExtraWidth);

        return () => {
            // height
            smallHeightQuery.removeEventListener("change", handleSmallHeight);
            mediumHeightQuery.removeEventListener("change", handleMediumHeight);
            largeHeightQuery.removeEventListener("change", handleLargeHeight);
            extraHeightQuery.removeEventListener("change", handleExtraHeight);

            // width
            smallWidthQuery.removeEventListener("change", handleSmallWidth);
            mediumWidthQuery.removeEventListener("change", handleMediumWidth);
            largeWidthQuery.removeEventListener("change", handleLargeWidth);
            extraWidthQuery.removeEventListener("change", handleExtraWidth);
        };
    }, []);

    return {
        // height
        isSmallHeight, // 0 - 640px
        isMediumHeight, // 641 - 768px
        isLargeHeight, // 769 - 1024px
        isExtraHeight, // 1025px+

        // width
        isSmallWidth, // 0 - 640px
        isMediumWidth, // 641 - 768px
        isLargeWidth, // 769 - 1024px
        isExtraWidth, // 1025px+
    };
};

export { useScreenSize };
