function findKeyByPathname(array, href) {
    for (let item of array) {
        if (item?.props?.href === href) {
            return item.props?.key;
        }
        if (item?.children && Array.isArray(item?.children)) {
            const result = findKeyByPathname(item.children, href);
            if (result) {
                return result;
            }
        }
    }
    return null;
}


function findByKey(array, key) {
    for (let item of array) {
        if (item?.props?.key === key) {
            return item;
        }
        if (item?.children && Array.isArray(item?.children)) {
            const result = findByKey(item.children, key);
            if (result) {
                return result;
            }
        }
    }
    return null;
}


function findKeyPath(array, key, path = []) {
    for (let item of array) {
        let currentPath = [...path, item.props.key];
        if (item?.props?.key === key) {
            return currentPath;
        }
        if (item?.children && Array.isArray(item?.children)) {
            const result = findKeyPath(item.children, key, currentPath);
            if (result) {
                return result;
            }
        }
    }
    return null;
}