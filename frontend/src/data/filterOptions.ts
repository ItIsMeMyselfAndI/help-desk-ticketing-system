const getYearOptions = () => {
    const curr = new Date();
    const currYear = Number(curr.toISOString().split("-")[0]);
    const years = Array<string>(200);
    for (let i = 0; i < 100; i++) {
        years.push(String(currYear - i));
    }
    return years;
};
const monthOptions = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export { getYearOptions, monthOptions };
