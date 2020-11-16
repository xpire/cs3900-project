export const makeSkeleton = (n) =>
  [...Array(n)].map((_) => {
    return { skeleton: true };
  });
