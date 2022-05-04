#include "imagepassthroughgadget.h"

namespace Gadgetron4Fun{

    ImagePassthroughGadget::ImagePassthroughGadget()
    {
    }

    ImagePassthroughGadget::~ImagePassthroughGadget() {
        // TODO Auto-generated destructor stub
    }

    int ImagePassthroughGadget::process_config(ACE_Message_Block* mb) {
        return 0;
    }


    int ImagePassthroughGadget::process(GadgetContainerMessage<ISMRMRD::ImageHeader> *m1, GadgetContainerMessage<hoNDArray<float> > *m2)
    {
        if (this->next()->putq(m1) < 0) {
            GDEBUG("Failed to pass on data to next Gadget\n");
            return GADGET_FAIL;
        }

        return GADGET_OK;
    }

    GADGET_FACTORY_DECLARE(ImagePassthroughGadget)

}