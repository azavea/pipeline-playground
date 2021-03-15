# The RV commit here only needs to be updated if RV has changed any dependencies
# since the last commit, which doesn't happen very often. Changing this commit
# will make building the image and publishing it take a long time, so it should
# only be updated if needed. For merely grabbing changes to the RV source code, the
# RV_SRC_COMMIT env var below should be updated.
FROM quay.io/azavea/raster-vision:pytorch-b6b91fb

# The RV commit here should be updated whenever we want to update the RV source code.
# After updating this commit, it should take very little time to build and
# publish the image. This commit should always be >= to the commit in the RV image that
# this Dockerfile inherits from.
ENV RV_SRC_COMMIT="b6b91fb331cae2d83886f795a87cc30e333af551"
RUN mkdir -p /tmp/rv && \
   cd /tmp/rv/ && \
   wget -q -O rv.zip https://github.com/azavea/raster-vision/archive/${RV_SRC_COMMIT}.zip && \
   unzip rv.zip && \
   cd raster-vision-${RV_SRC_COMMIT}* && \
   cp -r rastervision_* /opt/src/ && \
   cd /opt/src && \
   rm -r /tmp/rv/

COPY ./rv_kubeflow/ /opt/src/rv_kubeflow/
ENV PYTHONPATH=/opt/src/rv_kubeflow/:$PYTHONPATH

CMD ["bash"]
